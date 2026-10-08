"""
Vercel Serverless Function Entry Point for Flask Application.
Imports and exposes the Flask WSGI instance 'app' for Vercel deployment.
Includes robust path routing resolution for Vercel internal rewrites.
"""

import os
import sys

# Ensure the root project directory is on sys.path so app.py and local modules can be imported
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app as flask_app


class VercelWSGIProxy:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        headers_info = {
            k: v for k, v in environ.items()
            if k.startswith("HTTP_") or k in ("PATH_INFO", "REQUEST_URI", "RAW_URI")
        }
        print("VERCEL WSGI ENV:", headers_info)

        orig_path = (
            environ.get("HTTP_X_FORWARDED_URI") or
            environ.get("HTTP_X_MATCHED_PATH") or
            environ.get("REQUEST_URI") or
            environ.get("RAW_URI")
        )
        if orig_path:
            path_only = orig_path.split("?")[0]
            if path_only:
                environ["PATH_INFO"] = path_only
        elif environ.get("PATH_INFO", "").startswith("/api/index"):
            environ["PATH_INFO"] = "/"

        return self.wsgi_app(environ, start_response)


app = VercelWSGIProxy(flask_app)
