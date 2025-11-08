name: Auto-publish scheduled Jekyll posts

on:
  schedule:
    - cron: "*/5 * * * *"    # every 5 minutes
  workflow_dispatch:

permissions:
  contents: write

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml

      - name: Move due posts
        run: python .github/scripts/publish_due_posts.py

      - name: Commit & push if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          if [ -n "$(git status --porcelain)" ]; then
            git add -A
            git commit -m "[auto] Publish due posts"
            git push
          else
            echo "No changes."
          fi
