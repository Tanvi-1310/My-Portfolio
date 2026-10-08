# Tanvi Patil — Portfolio

A clean, modern, and responsive personal portfolio website showcasing web development projects, UI/UX designs, and applied AI applications. Built using Flask, Jinja2, vanilla CSS, and vanilla JavaScript with zero bloated framework dependencies.

---

## Overview

This repository contains the complete personal portfolio of Tanvi Patil. It features a custom soft pastel design system, a twilight dark theme, structured project showcases with handcrafted CSS visual motifs, verified certifications, an interactive contact form backed by SQLite/SQLAlchemy, and dynamic resume serving.

---

## Positioning

**Frontend Developer • UI/UX Enthusiast • AI Enthusiast**

> *"Crafting intentional, user-centered web interfaces with clean design systems, accessible interactions, and thoughtful AI-assisted workflows."*

---

## Tech Stack

- **Backend**: Python 3.10+, Flask 3.x, Flask-SQLAlchemy 3.x, Jinja2 template engine
- **WSGI / Production Server**: Gunicorn (for Linux/container deployment)
- **Database**: SQLite (default local development and lightweight persistence via SQLAlchemy ORM)
- **Frontend Core**: Semantic HTML5, Vanilla CSS3 (CSS custom properties, flexbox, CSS grid)
- **Frontend Scripting**: Vanilla JavaScript (ES6+, async/await fetch API, zero external libraries)
- **Design System**: Soft pastel lavender & rose palette with twilight dark mode and custom CSS visual motifs

---

## Features

- **Responsive Multi-Device Layout**: Fully tested and optimized across Desktop (1440×900), Laptop (1280×800), Tablet (768×1024), and Mobile (390×844) viewports without horizontal scrolling or text clipping.
- **Dual Theme Support**: Polished Light Theme (pastel lavender `#7353ba`, soft rose `#d36882`, off-white cards) and Twilight Dark Theme (`#171422` slate base with `#231f33` layered surfaces). The theme preference persists via `localStorage` with system `prefers-color-scheme` fallback.
- **Precision Anchor Navigation**: Sticky header with calibrated `scroll-margin-top` ensures section titles and badges land neatly below the navigation bar.
- **Mobile Navigation Drawer**: Accessible hamburger menu with focus management, backdrop dimming, and smooth transitions.
- **Projects Showcase**: Visual gallery showcasing 4 real projects with direct verified links: *POLAROPS — Antarctic Operational Digital Twin*, *StudentResume AI*, *Savora — Smart Restaurant Management System*, and *CRYOS — Polar Expedition Logistics*. Clean visual thumbnails, concise descriptions, and zero fabricated metrics.
- **Certifications**: Clean credential cards highlighting verified coursework across Object-Oriented Programming in Java, Python, Graph Data Structures, AI in Entrepreneurship, and Technical Debate.
- **Contact Form**: Interactive form with client-side validation, server-side data sanitization and length checks, and persistent storage in SQLite.
- **Dynamic Resume Routing**: Serves `resume.pdf` when placed in the assets folder, or displays an informative placeholder page.
- **SEO & Accessibility**: Semantic HTML structure, single `<h1>` hierarchy, meta description, Open Graph tags, descriptive ARIA attributes, SVG favicon, and custom 404/500 error pages.

---

## Project Structure

```text
My-Portfolio/
├── app.py                      # Flask application entry point, models, routes & data
├── requirements.txt            # Python dependencies (Flask, Flask-SQLAlchemy, gunicorn)
├── .env.example                # Example environment variables template
├── .gitignore                  # Git ignore rules for virtual environments, secrets, databases
├── README.md                   # Project documentation
├── instance/
│   └── portfolio.db            # Local SQLite database (git-ignored)
├── static/
│   ├── css/
│   │   └── style.css           # Design tokens, themes, layouts, and responsive card styling
│   ├── js/
│   │   └── script.js           # Theme toggle, mobile drawer, scroll spy, contact form submission
│   ├── images/                 # Project thumbnails (studentresume-ai.svg, polarops.svg, etc.)
│   └── assets/
│       ├── .gitkeep            # Directory placeholder
│       └── resume.pdf          # Place your real resume PDF here
└── templates/
    ├── base.html               # Base layout, header, footer, SEO tags, theme initialization
    ├── index.html              # Main single-page sections (Hero, About, Skills, Projects, Certs, Contact)
    ├── resume_placeholder.html # Graceful fallback page when resume.pdf is not yet present
    └── 404.html                # Custom error page matching design system
```

---

## Local Setup

### 1. Prerequisites

- Python 3.10 or higher
- Git (for version control)

### 2. Clone the Repository

```bash
git clone https://github.com/Tanvi-1310/My-Portfolio.git
cd My-Portfolio
```

### 3. Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables (Optional for Local Dev)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

*(On Windows PowerShell, use `Copy-Item .env.example .env`)*

### 6. Run the Application

```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## Environment Variables

The application reads configuration from environment variables with sensible local defaults:

| Variable | Description | Default (Local) | Production Example |
|---|---|---|---|
| `SECRET_KEY` | Secret key for Flask session signing | `dev-fallback-key-...` | A strong 64-character random string |
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///instance/portfolio.db` | `postgresql://user:pass@host:5432/dbname` |
| `FLASK_DEBUG` | Enable debug mode (`1` or `0`) | `0` (Off) | `0` |
| `PORT` | Local server port | `5000` | Assigned by cloud host (e.g., Render/Railway) |

Refer to `.env.example` for the starter template. **Never commit `.env` or production credentials to Git.**

---

## Resume

The application includes an automated resume handler:

1. **To publish your real resume**: Place your PDF file at:
   ```text
   static/assets/resume.pdf
   ```
2. **Behavior**:
   - If `static/assets/resume.pdf` exists: Visiting `/resume` or clicking "Download Resume" in the UI immediately streams the real PDF document.
   - If `static/assets/resume.pdf` does not exist: Visiting `/resume` serves a transparent placeholder page informing visitors that the document is being finalized, while offering direct navigation back to Projects and Contact.

---

## Contact Form & Local Database

The contact form submits asynchronously via `fetch` to `POST /contact`:

1. **Validation**: Server-side checks ensure name (2–100 chars), a valid email address format, and message content (10–2000 chars).
2. **Storage**: Valid submissions are saved directly to `instance/portfolio.db` via the SQLAlchemy `ContactMessage` model.
3. **Database Privacy**: The `instance/` folder and all `*.db` files are strictly excluded in `.gitignore` to prevent committing visitor data or local databases to version control.

---

## Testing

A functional test script validates key routes, HTTP status codes, form validation, and database operations.

To run tests:

```bash
python -m unittest discover -s . -p "test_*.py"
```

Or execute direct route verification against the running server:
- `GET /` — Returns HTTP 200 (renders homepage)
- `GET /resume` — Returns HTTP 200 (placeholder or PDF)
- `GET /favicon.ico` — Returns HTTP 200 with `image/svg+xml`
- `GET /contact` — Returns HTTP 302 redirecting to `/#contact`
- `POST /contact` (invalid body) — Returns HTTP 400 with validation JSON errors
- `POST /contact` (valid body) — Returns HTTP 200 with confirmation JSON and persists record
- `GET /non-existent-route` — Returns HTTP 404 with custom themed error template

---

## Deployment

### Vercel Deployment

This Flask portfolio is optimized for zero-config serverless deployment on **Vercel**:

1. **Connect GitHub Repository**:
   - Go to [vercel.com](https://vercel.com) and import your `My-Portfolio` repository.
   - Vercel automatically detects the Python runtime via `vercel.json` and `api/index.py`.

2. **Configure Environment Variables**:
   In your Vercel Project Settings under **Environment Variables**, add:
   - `SECRET_KEY`: A strong 64-character random string (e.g. generate via `python -c "import secrets; print(secrets.token_hex(32))"`).
   - `FLASK_DEBUG`: Set to `0` (production).
   - `DATABASE_URL`: Your persistent PostgreSQL connection string (e.g. from Vercel Postgres, Supabase, Neon, or Neon Postgres).

3. **Deploy**:
   - Click **Deploy**. Vercel will install dependencies from `requirements.txt` and package templates and static assets into the serverless function.

> **Important Database Note**:
> - **SQLite is intended for local development.** In Vercel serverless functions, the local filesystem is read-only and ephemeral.
> - **Use PostgreSQL for production contact submissions.** Configure `DATABASE_URL=postgresql://...` so contact inquiries persist permanently.

---

## Project Status

- **Development Phase**: Release Ready — Prepared and Verified for Vercel Serverless Deployment.
- **Project Links**: All featured projects feature direct verified links (`Live Demo ↗` and `GitHub ↗`) without dummy URLs or fabricated stats.
- **Visual Presentation**: Project-specific illustrative vector visual compositions provide authentic, honest context for each real project.
