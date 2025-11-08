#!/usr/bin/env python3
import re, sys
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCHEDULED = ROOT / "_scheduled"
POSTS = ROOT / "_posts"
LOCAL_TZ = ZoneInfo("America/Chicago")  # your timezone

FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-{2,}', '-', s).strip('-')
    return s or "post"

def parse_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text = m.group(1)
    body = text[m.end():]
    data = yaml.safe_load(fm_text) or {}
    return data, body

def render_frontmatter(data: dict) -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False).strip() + "\n---\n"

def to_dt(obj):
    s = str(obj)
    # Try "YYYY-MM-DD HH:MM"
    try:
        dt = datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=LOCAL_TZ)
        return dt
    except ValueError:
        pass
    # Fallback: ISO; add local tz if naive
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LOCAL_TZ)
    return dt

def due_files():
    if not SCHEDULED.exists():
        return []
    now_utc = datetime.now(timezone.utc)
    out = []
    for p in list(SCHEDULED.glob("*.md")) + list(SCHEDULED.glob("*.markdown")):
        text = p.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        pa = fm.get("publish_at")
        if not pa:
            continue
        try:
            when = to_dt(pa)
        except Exception:
            continue
        if now_utc >= when.astimezone(timezone.utc):
            out.append((p, fm, body, when))
    return out

def main():
    POSTS.mkdir(exist_ok=True)
    changed = False
    for path, fm, body, when in due_files():
        title = fm.get("title") or path.stem
        slug = slugify(title)
        date_for_filename = when.astimezone(LOCAL_TZ).strftime("%Y-%m-%d")
        out_name = f"{date_for_filename}-{slug}{path.suffix}"
        out_path = POSTS / out_name

        # Update frontmatter date to full ISO timestamp
        fm["date"] = when.astimezone(LOCAL_TZ).isoformat()
        # Remove publish_at so it doesn’t linger
        fm.pop("publish_at", None)

        new_text = render_frontmatter(fm) + body
        out_path.write_text(new_text, encoding="utf-8")
        path.unlink()
        print(f"Published: {out_path.relative_to(ROOT)}")
        changed = True

    # Let the workflow know if anything changed
    if changed:
        (ROOT / ".last_publish_run").write_text(datetime.now().isoformat(), encoding="utf-8")
    return 0

if __name__ == "__main__":
    sys.exit(main())
