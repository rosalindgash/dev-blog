---
layout: post
title: "How I Built My First SaaS App: The Story Behind PingBuoy"
date: 2025-10-30
tags: [SaaS, Solo-Founder, AI-Development, Case-Study]
excerpt: "The honest story of building a website monitoring SaaS across 54 development sessions. No overnight success here—just real development with all its challenges, setbacks, and victories."
featured: true
---

If you've spent any time on Twitter or LinkedIn lately, you've probably seen posts like: "Built a $10k/month SaaS in a weekend!" or "From idea to launch in 48 hours!"

Let me tell you something: that's not how this works.

This is the story of building PingBuoy, a website monitoring SaaS application, across 54 development sessions spanning a month. It's a story of small victories, frustrating setbacks, and the reality of modern web development. If you're thinking about building your own SaaS, this article will give you an honest look at what it actually takes.

**Spoiler alert:** You need coding experience. Not expert-level, but some amount of real coding knowledge is absolutely necessary. The "tech bros" who claim anyone can build a SaaS overnight are either lying or selling something. That said, with some programming background and persistence, you can definitely do this.

## What I Built

PingBuoy is a website monitoring platform that helps website owners know when their sites go down. Think of it as a watchdog for your website that:

- Checks if your site is online every 1-5 minutes (depending on your plan)
- Scans for broken links across your pages
- Sends email alerts when something goes wrong
- Provides charts showing your site's uptime history
- Offers public status pages you can share with users

The app includes everything you'd expect from a modern SaaS: user authentication, tiered pricing (free and pro plans), Stripe billing integration, and a polished dashboard interface.

## The Development Process: Human + AI Collaboration

Before we dive into the technical details, I need to be honest about how this was built: **I didn't write most of the code myself.**

I used Claude Code (Anthropic's AI coding assistant) as my primary development partner. Think of it this way:

- **I was the architect** - I made all the decisions about what to build, which technologies to use, and how the system should work
- **Claude Code was the construction crew** - It wrote the actual code, implemented features, and handled the tedious parts

But here's the thing: Claude Code gets stuck. A lot. It goes down wrong paths, makes assumptions, and sometimes implements things completely differently than I intended. My job was to:

- Guide it when it went off track
- Debug issues it couldn't figure out
- Make architectural decisions when it proposed bad solutions
- Review all code before accepting it
- Step in and write code manually when Claude Code was struggling

I'm not going to lie and say I just typed "build me a SaaS" and it appeared. This required **real coding knowledge** to guide the AI, catch its mistakes, and know when to override its suggestions. The AI accelerated development significantly, but it didn't eliminate the need for programming skills.

This is the reality of AI-assisted development in 2025: it's powerful, but you still need to know what you're doing.

## The Tech Stack: Modern But Practical

I built PingBuoy using:

- **Next.js 15** with TypeScript for the frontend and backend
- **Supabase** for the PostgreSQL database and authentication
- **Stripe** for payment processing
- **Tailwind CSS** for styling
- **Nodemailer** for email notifications

Why these choices? They're modern, well-documented, and have active communities. When you inevitably get stuck (and you will), having good documentation and Stack Overflow answers is worth its weight in gold.

## The Beginning: Excitement and Naive Optimism

**Sessions 1-4** | *September 8-9, 2025*

I decided I was going to use Claude Code, so the first thing I had to do was install it. So, I opened up Windows PowerShell and typed:

```bash
npm install -g @anthropic-ai/claude-code
```

Then I navigated to my project folder on my hard drive. I started with a PDF planning document outlining all the features I wanted and told Claude Code to help me create the app.

It created a comprehensive todo list with 15 major features and got to work creating authentication, monitoring, dead link detection, billing, and deployment. Everything seemed to be going excellently and I thought my app would be complete in just a few sessions.

"Wow!" I remember thinking, "This really is as easy as they say it is!"

It's not.

The first real challenge hit immediately: port conflicts. My development port was already in use. Small problem, easy fix, but a sign of things to come. Then came DNS resolution issues with Supabase's domain. I spent an hour debugging before realizing my Windows/WSL2 setup was causing problems.

> **Lesson 1:** Development environment issues will eat your time. Set up your environment properly before you start coding.

## The Core Build: When Things Feel Good

**Sessions 5-7** | *September 10, 2025*

These sessions were the honeymoon phase. I built out the main components:

- Dashboard with site monitoring
- Authentication pages (login, signup, password reset)
- API routes for site management
- Uptime monitoring logic
- Dead link scanner

The code felt clean and worked on the first try. These moments make you feel like a coding wizard. Enjoy them, because they don't last.

## The Database Saga: A Cautionary Tale

**Sessions 8-14** | *September 12-14, 2025*

This is where things got messy. I needed to set up database migrations properly with Supabase. Simple, right?

Nope.

I encountered what I now call "migration hell." My local migration files didn't match the remote database's migration history. I had multiple backup folders (`migrations_backup_*`, `migrations_off`, `.temp`) with no clear source of truth. The error messages were cryptic:

```
Error: Remote migration history differs from local

Expected: 20250912000001_create_core_tables.sql

Found: create_core_tables.sql
```

After two full sessions of struggling, I made a bold decision: **start fresh**. Claude Code quarantined everything:

```bash
mv supabase supabase_quarantine
supabase init
```

Then it carefully reviewed the old migrations, extracted the ones that actually changed the schema, renamed them with proper timestamps, and rebuilt the migration history from scratch.

> **Lesson 2:** When your database migrations are a mess, don't try to patch it. Quarantine the old files (don't delete them—you might need them for reference) and rebuild cleanly.

The proper way to name migrations:

```
20250912143022_create_core_tables.sql  ← Good (YYYYMMDDHHMMSS_description)
create_core_tables.sql                  ← Bad (no timestamp)
migration_v2.sql                        ← Bad (vague naming)
```

## Security: The Never-Ending Story

**Sessions 15-18, 28-35** | *September 14-24, 2025*

Security consumed way more time than I expected. I implemented:

1. **Row Level Security (RLS)** - So users can only access their own data
2. **Content Security Policy (CSP)** - To prevent XSS attacks
3. **Input validation** - To stop SQL injection
4. **Rate limiting** - To prevent abuse

Simple enough. But then RLS started **blocking my authentication flows**. Users (me, on a test account) couldn't log in because RLS was preventing the auth system from querying user data. It was a chicken-and-egg problem.

The fix required carefully designed policies that checked for authenticated sessions while still allowing the auth flow to complete. This took three sessions to get right.

### The CSP Nightmare

Content Security Policy deserves its own section because it broke **three separate times** during development. Each time I thought it was fixed, it would break again when I added a new feature.

The problem with CSP is that modern web apps pull resources from everywhere:

- Stripe for payment forms
- Supabase for database connections
- Google Analytics for tracking
- WebSocket connections for real-time updates

Each integration needs to be explicitly allowed in your CSP header. Miss one, and your app breaks in subtle ways.

I eventually implemented a nonce-based CSP system.

> **Lesson 3:** Security is not a one-time task. Budget significant time for security implementation and testing. And when CSP breaks (not if, when), check your browser console's security tab (F12).

## The Authentication Redirect Loop: A Detective Story

**Sessions 19-27** | *September 21-23, 2025*

Picture this: Users can enter their email, receive the magic link, click it, and then... get redirected back to the login page. Over and over.

I spent **nine sessions** tracking down this bug. Nine sessions. Here were the suspects:

1. **CSP blocking JavaScript** - Partially true, fixed it
2. **Middleware misconfiguration** - Checked, seemed fine
3. **RLS blocking auth queries** - Adjusted policies
4. **Client-side DNS issues** - Bingo... sort of

The reality was that the bug had **multiple causes**. Fixing CSP helped. Adjusting RLS helped. But the final piece was a DNS resolution issue in my Windows/WSL2 environment that prevented the Supabase client from connecting properly.

The fix required proper client initialization and proper session handling.

> **Lesson 4:** When debugging complex issues, assume multiple causes. Don't stop after fixing one thing—verify the entire flow works end-to-end.

## The Great Architecture Pivot

**Sessions 36-45** | *September 25-October 1, 2025*

Originally, I built the monitoring system using Supabase Edge Functions. The idea was simple: serverless functions that check websites every few minutes and log the results.

But Edge Functions came with problems:

- Complex deployment process
- Secret management headaches
- Difficult to debug
- Slower response times
- Additional points of failure

After struggling with this for a week, and finally consulting Claude AI, I made a significant architectural decision: **move monitoring into the database itself**.

This change **simplified the entire architecture**. Fewer moving parts. Easier debugging. Better performance.

> **Lesson 5:** Don't be afraid to pivot on architectural decisions. If something is consistently causing problems, there might be a simpler approach.

## Stripe Integration: The One Thing That Just Worked

**Sessions 6-7, 42**

Not everything was hard. The Stripe integration was surprisingly smooth. Claude Code sailed right through this one.

> **Lesson 6:** Good documentation and tooling make all the difference. Stripe nailed it.

## The Dashboard: Making Data Visual

**Sessions 6-7, 40-42**

The dashboard needed to show uptime history in an engaging way. I used Recharts for visualization. Seeing the charts come to life was one of the most satisfying moments of the project.

This is where it starts to feel like a real product.

## Email Notifications: Harder Than Expected

**Sessions 8, 44-45**

You'd think sending emails would be straightforward. It's not.

I had to implement:

- Email template rendering
- Rate limiting (to prevent spam)
- Delivery tracking
- Retry logic for failed sends
- Proper error handling

Without rate limiting, a site with frequent downtime could trigger hundreds of emails per hour. That's a fast way to get your email domain blacklisted.

> **Lesson 7:** Email is a complex system. Budget time for proper implementation with rate limiting, logging, and error handling.

## The Final Stretch: Production Readiness

**Sessions 46-54** | *October 1+, 2025*

The last sessions were about polish and cleanup:

- Removing unused Edge Functions
- Fixing console errors
- Final security audits
- Environment variable documentation
- Deployment configuration

This phase revealed dozens of small issues that didn't show up in development:

- Empty error objects being logged
- Missing null checks causing crashes
- Race conditions in real-time updates
- Memory leaks in long-running processes

Each fix was small, but collectively they made the difference between a demo and a production app.

## What I Learned: The Honest Truth

### It Takes Longer Than You Think

My initial estimate: 2 weeks

The reality: 5 weeks working ~3.5 hours per day

**Total cost:** ~$200 for Claude AI Max access, plus $20/mo for Vercel hosting.

Even with AI assistance and modern frameworks, building a production-ready SaaS is a significant undertaking.

### Some Things Are Just Hard

No matter how good your tools are, certain problems are inherently complex:

- Security (RLS, CSP, authentication)
- Database migrations
- Asynchronous operations
- Multi-tenant architecture
- Email deliverability

These aren't "solve once and forget" problems. They require ongoing attention.

### You Need Real Coding Skills

Let me be clear: you can't build this without programming knowledge - you at least need to be able to recognize when code looks wrong or doesn't make (logical) sense. You need to understand, or be willing to learn on the fly:

- How web requests work
- Database relationships and SQL
- Asynchronous JavaScript
- React component lifecycle
- API design
- Security principles

The "no-code" tools might get you a basic landing page, but a real SaaS requires real coding.

### The Dev Environment Matters

I lost hours to Windows/WSL2 quirks:

- Path resolution issues
- Port conflicts
- DNS problems
- File permission errors

If you're serious about web development, invest time in setting up your environment properly. As of writing this article, you can now use Claude Code in your web browser.

### Good Documentation Is Worth Gold

The technologies with great docs (Stripe, Tailwind) were a joy to work with. The ones with poor documentation caused disproportionate frustration. It's true that AI coding assistants don't experience frustration. However, as your project's architect you may have to consult documentation yourself and the better it's written the easier it is to understand.

When choosing your tech stack, consider documentation quality as a primary factor.

### Architectural Decisions Matter

The pivot from Edge Functions to database-level monitoring saved the project. The right architecture can make the difference between constant fighting and smooth development.

Don't be dogmatic about your initial choices. If something isn't working, be willing to change course.

### Security Can't Be Bolted On

I tried to add security after building core features. Big mistake. Security needs to be designed in from the start:

- Authentication flows
- Data access patterns
- Input validation
- Error handling

Retrofitting security is painful and error-prone.

## The Reality Check: Should You Build a SaaS?

After 54 sessions and countless hours, here's my honest take:

**You should build a SaaS if:**

- You have a genuine understanding of programming
- You're comfortable with modern web technologies
- You can debug complex issues systematically
- You're willing to spend months on development
- You have realistic expectations about time and complexity
- You enjoy solving technical problems

**You probably shouldn't build a SaaS if:**

- You're expecting to build it in a weekend
- You don't want to write any code
- You're not willing to learn continuously
- You give up when things get difficult
- You believe the "anyone can do it" hype

## Final Thoughts

Building PingBuoy was hard. Harder than I expected. There were moments of frustration where I questioned whether it was worth it and there were times when I wanted to quit.

But there were also moments of pure joy:

- Seeing the first successful uptime check
- Watching the charts render real data
- Receiving the first Stripe test payment
- Fixing that nine-session authentication bug

If you're thinking about building your own SaaS, go for it. But go in with your eyes open. It's not a weekend project. It's not easy. The "tech bros" on Twitter and YouTube are selling you a fantasy.

The reality is messy database migrations, CSP violations at 2 AM, and authentication bugs that take nine sessions to fix.

But if you're willing to put in the work, to learn continuously, to debug systematically, and to iterate patiently—you can absolutely build something real.

Just don't believe anyone who tells you it's easy.

## Try PingBuoy

If you want to see the result of these 54 sessions, PingBuoy is live at [pingbuoy.com](https://pingbuoy.com). The free plan monitors 2 websites with checks every 10 minutes - no credit card required.

## How This Article Was Written

In keeping with the AI-assisted theme, this article itself was generated through an interesting process:

1. **Extracted the logs**: All 54 Claude Code sessions were saved as `.jsonl` files (JSON Lines format) by default
2. **Converted to readable format**: I built a pipeline (`master_pipeline.py`) that renamed the session files and converted them to Markdown and HTML
3. **Fed them back to Claude Code**: I gave Claude Code access to all 54 session transcripts and asked it to write this article
4. **Edited for accuracy**: I reviewed and edited to add context and ensure the narrative was accurate

Even this article required human oversight - Claude Code did the heavy lifting of synthesizing 54 sessions worth of conversations, but I had to:

- Clarify the human-AI collaboration dynamic (which it initially missed)
- Verify technical accuracy
- Add emotional context and personal reflections
- Adjust the tone in places

It's AI-assisted writing about AI-assisted development. Meta? Yes. But also a perfect example of how human-AI collaboration actually works.
