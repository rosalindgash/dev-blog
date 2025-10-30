# Rosalind Gash - The Dev Blog

A clean, minimalist Jekyll blog for documenting solo SaaS development, AI-assisted coding, and tech entrepreneurship.

## Quick Start

### 1. Set Up Repository

```bash
# Create a new GitHub repository named: username.github.io
# (Replace 'username' with your GitHub username)

# Clone and add your blog files
git clone https://github.com/username/username.github.io.git
cd username.github.io
# Copy all files from this jekyll-blog folder to your repo
```

### 2. Update Configuration

Edit `_config.yml` and update:
```yaml
url: "https://yourusername.github.io"  # Your actual GitHub Pages URL
```

### 3. Push to GitHub

```bash
git add .
git commit -m "Initial blog setup"
git push origin main
```

GitHub Pages will automatically build your site! Visit `https://yourusername.github.io` in a few minutes.

## Writing Posts

### Create a New Post

1. Create a new file in `_posts/` folder
2. Name it: `YYYY-MM-DD-title-of-post.md`
3. Add front matter and content

### Post Template

```markdown
---
layout: post
title: "Your Article Title Here"
date: 2025-10-30
tags: [AI-Development, Solo-Founder, SaaS]
excerpt: "A short description that appears in the blog grid"
featured: false  # Set to true for the featured post on home page
---

Your article content here in Markdown...

## Section Heading

Regular paragraphs...

### Subsection

- Bullet points
- More bullets

```code blocks```
```

### Markdown Syntax Guide

```markdown
# H1 Heading
## H2 Heading
### H3 Heading

**Bold text**
*Italic text*

[Link text](https://example.com)

- Unordered list item
- Another item

1. Ordered list item
2. Another item

`inline code`

\`\`\`python
# Code block
def hello():
    print("Hello world")
\`\`\`

> Blockquote text
```

## Common Tags

Use these tags consistently:
- `AI-Development`
- `Solo-Founder`
- `SaaS`
- `Database`
- `Security`
- `Product`
- `PostgreSQL`
- `Monitoring`
- `Testing`
- `CI-CD`

## Features

✅ **Automatic pagination** - Shows 6 posts per page
✅ **Social sharing** - Twitter, Facebook, LinkedIn, Reddit buttons on every post
✅ **Tags system** - Automatic tag collection and display
✅ **Featured posts** - Highlight your best content
✅ **Responsive design** - Mobile-friendly
✅ **SEO optimized** - Meta tags and structured data
✅ **Fast loading** - Minimal, efficient CSS

## Local Development (Optional)

If you want to preview locally before pushing:

```bash
# Install Ruby and Jekyll (one-time setup)
gem install bundler jekyll

# Install dependencies
bundle install

# Run local server
bundle exec jekyll serve

# Visit http://localhost:4000
```

## Folder Structure

```
jekyll-blog/
├── _config.yml          # Site configuration
├── _layouts/            # Page templates
│   ├── default.html     # Base layout
│   └── post.html        # Individual post layout
├── _includes/           # Reusable components
│   ├── navigation.html
│   └── footer.html
├── _posts/              # Your blog posts (Markdown)
│   └── 2025-10-30-building-pingbuoy.md
├── assets/
│   └── css/
│       └── style.css    # All your styles
├── index.html           # Home page
├── Gemfile              # Ruby dependencies
└── .gitignore
```

## Tips

1. **Consistent naming**: Always use `YYYY-MM-DD-title.md` for post filenames
2. **Excerpts**: Keep them under 160 characters for best display
3. **Featured post**: Only mark ONE post as `featured: true`
4. **Images**: Store in `assets/images/` and reference with `/assets/images/filename.jpg`
5. **Test locally**: Use `jekyll serve` to preview before pushing

## Troubleshooting

**Site not showing up?**
- Check that your repo is named `username.github.io`
- Wait 2-3 minutes after pushing
- Go to Settings → Pages and ensure GitHub Pages is enabled

**Posts not appearing?**
- Check filename format: `YYYY-MM-DD-title.md`
- Ensure front matter is between `---` lines
- Verify date isn't in the future

**Styling looks broken?**
- Check that `style.css` is in `assets/css/`
- Clear browser cache
- Check browser console for errors

## Need Help?

Common issues:
1. Date format in filename must be exact
2. Front matter must have proper YAML syntax
3. Tags should be in a list format: `[Tag1, Tag2]`

## What's Next?

1. Write your first post based on the example
2. Customize colors in `assets/css/style.css`
3. Add your actual content
4. Share your blog URL!

Happy writing! 🚀
