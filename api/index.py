"""
Vercel Serverless Function Entry Point for Flask Application.
Imports and exposes the Flask WSGI instance 'app' for Vercel deployment.
"""

import os
import sys

# Ensure the root project directory is on sys.path so app.py and local modules can be imported
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app
