"""
Vercel Serverless Function Entry Point for Flask Application.
Imports and exposes the Flask WSGI instance 'app' for Vercel deployment.
Includes robust path routing resolution for Vercel internal rewrites.
"""

import os
import sys
from urllib.parse import parse_qs, urlencode

# Ensure the root project directory is on sys.path so app.py and local modules can be imported
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app as flask_app


class VercelWSGIProxy:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = environ.get("QUERY_STRING", "")
        if "__path__=" in qs:
            params = parse_qs(qs, keep_blank_values=True)
            if "__path__" in params:
                raw_path = params.pop("__path__")[0]
                real_path = "/" + raw_path.lstrip("/")
                environ["PATH_INFO"] = real_path
                environ["QUERY_STRING"] = urlencode(params, doseq=True)
        elif environ.get("PATH_INFO", "").startswith("/api/index"):
            environ["PATH_INFO"] = "/"

        return self.wsgi_app(environ, start_response)


app = VercelWSGIProxy(flask_app)
