"""
Tanvi Patil - Personal Developer Portfolio
Flask Application Entry Point (Production & Release Ready)
Includes SQLite message storage, parameter validation, modular templates, and clean routing.
"""

import os
import re
from datetime import datetime, timezone
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    send_from_directory,
    Response
)
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# Security & App Configuration (Environment-Based)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-fallback-key-replace-with-env-in-production"
)

# Database Configuration: Persistent PostgreSQL in production, SQLite locally
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if db_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
else:
    # Local development SQLite fallback:
    # In serverless environments like Vercel with read-only root, use /tmp directly.
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        sqlite_path = os.path.join("/tmp", "portfolio.db")
    else:
        try:
            os.makedirs(app.instance_path, exist_ok=True)
            sqlite_path = os.path.join(app.instance_path, "portfolio.db")
        except OSError:
            sqlite_path = os.path.join("/tmp", "portfolio.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqlite_path}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database Instance
db = SQLAlchemy(app)


# Lightweight SQLite / PostgreSQL Model for Contact Inquiries
class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


# Initialize Database Tables Safely
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        app.logger.warning(f"Database initialization notice: {e}")


# Portfolio Structured Data Model
PORTFOLIO_DATA = {
    "profile": {
        "name": "Tanvi Patil",
        "first_name": "Tanvi",
        "brand": "Tanvi.",
        "role": "Frontend Developer • UI/UX Enthusiast • AI Enthusiast",
        "tagline_badges": [
            "Frontend Developer",
            "UI/UX Enthusiast",
            "AI Enthusiast"
        ],
        "hero_greeting": "Hello, I'm Tanvi.",
        "hero_title": "Frontend Developer • UI/UX Enthusiast • AI Enthusiast",
        "hero_sentence": "I enjoy turning ideas into clean, useful interfaces and exploring how AI can make digital products smarter.",
        "about_intro": "I'm Tanvi, an Information Technology Engineering student who enjoys building interfaces that are simple, useful, and visually thoughtful.",
        "about_focus": "My main focus is frontend development and UI/UX, while I explore AI through projects that solve practical problems.",
        "focus_summary": "Frontend • UI/UX • AI",
        "education": "B.E. Information Technology",
        "currently_learning": "React, TypeScript, Next.js, Design Systems",
        "github_url": "https://github.com/Tanvi-1310",
    },
    "skills": {
        "Frontend": [
            {"name": "HTML5", "icon": "html5"},
            {"name": "CSS3", "icon": "css3"},
            {"name": "JavaScript", "icon": "js"},
            {"name": "TypeScript", "icon": "ts"},
            {"name": "React", "icon": "react"}
        ],
        "Backend": [
            {"name": "Python", "icon": "python"},
            {"name": "Flask", "icon": "flask"},
            {"name": "Java", "icon": "java"},
            {"name": "Spring Boot", "icon": "springboot"}
        ],
        "Tools / Design / Data": [
            {"name": "Git", "icon": "git"},
            {"name": "Vite", "icon": "vite"},
            {"name": "Tailwind CSS", "icon": "tailwind"},
            {"name": "shadcn/ui", "icon": "shadcn"},
            {"name": "SQL", "icon": "sql"},
            {"name": "UI/UX", "icon": "figma"}
        ]
    },
    "projects": [
        {
            "id": "polarops",
            "title": "POLAROPS — Antarctic Operational Digital Twin",
            "description": "An Antarctic operational digital twin for route planning, environmental hazard awareness, and polar station logistics.",
            "technologies": ["React", "TypeScript", "FastAPI", "PostgreSQL"],
            "image": "polarops.svg",
            "image_alt": "POLAROPS Antarctic operational digital twin interface",
            "github_url": "https://github.com/Kshitij2011-spec/polarops",
            "demo_url": "https://polarops-two.vercel.app/",
            "is_featured": True
        },
        {
            "id": "studentresume-ai",
            "title": "StudentResume AI",
            "description": "An intelligent resume analyzer helping students structure technical resumes, align skills, and improve formatting clarity.",
            "technologies": ["React", "Python", "Flask", "NLP"],
            "image": "studentresume-ai.svg",
            "image_alt": "StudentResume AI resume analysis interface",
            "github_url": "https://github.com/Tanvi-1310/Student_Resume_Analyzer",
            "demo_url": "https://student-resume-analyzer.onrender.com",
            "is_featured": False
        },
        {
            "id": "savora",
            "title": "Savora — Smart Restaurant Management System",
            "description": "A restaurant management system coordinating floor table allocations, real-time dining orders, and kitchen ticket workflows.",
            "technologies": ["React", "TypeScript", "Vite", "Tailwind CSS"],
            "image": "savora.svg",
            "image_alt": "Savora smart restaurant management interface",
            "github_url": "https://github.com/Tanvi-1310/Savora",
            "demo_url": None,
            "is_featured": False
        },
        {
            "id": "cryos",
            "title": "CRYOS — Polar Expedition Logistics",
            "description": "A polar expedition logistics platform for traverse route planning, waypoint corridors, and remote field asset coordination.",
            "technologies": ["React", "TypeScript", "Tailwind CSS", "Vite"],
            "image": "cryos.svg",
            "image_alt": "CRYOS polar expedition logistics and waypoint planning interface",
            "github_url": "https://github.com/Kshitij2011-spec/CRYOS",
            "demo_url": "https://cryos-weld.vercel.app/",
            "is_featured": False
        }
    ],
    "certifications": [
        {
            "title": "OOPs in Java",
            "issuer": "Simplilearn",
            "icon": "code",
            "accent": "lavender"
        },
        {
            "title": "Introduction to Python",
            "issuer": "Infosys",
            "icon": "terminal",
            "accent": "blush"
        },
        {
            "title": "Graph Data Structure",
            "issuer": "Infosys",
            "icon": "share-2",
            "accent": "peach"
        },
        {
            "title": "AI in Entrepreneurship",
            "issuer": "Intel Skill India",
            "icon": "cpu",
            "accent": "lilac"
        },
        {
            "title": "Techbate",
            "issuer": "IETE",
            "icon": "award",
            "accent": "softblue"
        }
    ]
}


def check_resume_exists():
    """Checks whether static/assets/resume.pdf is physically present."""
    static_folder = app.static_folder or os.path.join(app.root_path, "static")
    resume_path = os.path.join(static_folder, "assets", "resume.pdf")
    return os.path.isfile(resume_path)


@app.context_processor
def inject_global_template_vars():
    """Injects current year and resume availability into all templates."""
    return {
        "current_year": datetime.now(timezone.utc).year,
        "has_resume": check_resume_exists()
    }


# ==============================================================================
# ROUTES
# ==============================================================================

@app.route("/")
@app.route("/api/index.py")
@app.route("/api/index.py/")
def home():
    """Renders the main single-page portfolio with all sections."""
    return render_template(
        "index.html",
        profile=PORTFOLIO_DATA["profile"],
        skills=PORTFOLIO_DATA["skills"],
        projects=PORTFOLIO_DATA["projects"],
        certifications=PORTFOLIO_DATA["certifications"]
    )


@app.route("/resume")
def resume():
    """
    Serves verified resume if present in static/assets/resume.pdf,
    otherwise renders the dedicated polished placeholder template.
    """
    static_folder = app.static_folder or os.path.join(app.root_path, "static")
    resume_path = os.path.join(static_folder, "assets", "resume.pdf")

    if os.path.isfile(resume_path):
        return send_from_directory(
            os.path.join(static_folder, "assets"),
            "resume.pdf",
            as_attachment=False
        )

    return render_template(
        "resume_placeholder.html",
        profile=PORTFOLIO_DATA["profile"]
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Handles contact inquiries.
    GET: Redirects to the homepage anchor #contact.
    POST: Validates inputs, saves to SQLite database, and returns truthful status.
    """
    if request.method == "GET":
        return redirect(url_for("home") + "#contact")

    # POST handling
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    errors = {}

    # Validation: Name
    if not name:
        errors["name"] = "Name is required."
    elif len(name) < 2 or len(name) > 100:
        errors["name"] = "Name must be between 2 and 100 characters."

    # Validation: Email
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not email:
        errors["email"] = "Email address is required."
    elif len(email) > 120 or not re.match(email_regex, email):
        errors["email"] = "Please provide a valid email address."

    # Validation: Message
    if not message:
        errors["message"] = "Message is required."
    elif len(message) < 10:
        errors["message"] = "Message must be at least 10 characters long."
    elif len(message) > 2000:
        errors["message"] = "Message cannot exceed 2000 characters."

    if errors:
        return jsonify({
            "success": False,
            "errors": errors,
            "message": "Please correct the highlighted errors."
        }), 400

    # Store message safely in SQLite using parameterized ORM
    try:
        new_inquiry = ContactMessage(
            name=name,
            email=email,
            message=message,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(new_inquiry)
        db.session.commit()

        # Truthful confirmation message (no false claim of third-party dispatch)
        response_text = (
            f"Thank you, {name}! Your message has been safely received and stored. "
            "I appreciate you reaching out and will get back to you as soon as possible."
        )

        return jsonify({
            "success": True,
            "message": response_text,
            "inquiry_id": new_inquiry.id
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred while saving your message. Please try again later."
        }), 500


@app.route("/favicon.ico")
def favicon():
    """Serves inline SVG favicon to prevent 404 console errors."""
    svg_icon = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<rect width="100" height="100" rx="24" fill="#7353ba"/>'
        '<text x="50" y="66" font-family="sans-serif" font-size="54" '
        'font-weight="bold" fill="#ffffff" text-anchor="middle">T</text>'
        '</svg>'
    )
    return Response(svg_icon, mimetype="image/svg+xml")


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page matching portfolio aesthetics."""
    return render_template(
        "404.html",
        profile=PORTFOLIO_DATA["profile"]
    ), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Custom 500 error page handling."""
    return render_template(
        "404.html",
        profile=PORTFOLIO_DATA["profile"]
    ), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true")
    app.run(host="127.0.0.1", port=port, debug=debug_mode)
