"""Local HTTP server that serves the snap animation and listens for the snap callback."""

import http.server
import os
import threading
import webbrowser
from functools import partial
from pathlib import Path


class _SnapHandler(http.server.SimpleHTTPRequestHandler):
    """Serves snap/ files and handles the POST /snapped callback from JS."""

    def do_POST(self):
        if self.path == "/snapped":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
            self.server.snap_event.set()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        pass  # suppress request logs


def _find_snap_dir() -> str:
    """Locate the snap/ directory containing the animation."""
    candidates = [
        Path(__file__).parent / "snap",          # installed inside package
        Path(__file__).parent.parent / "snap",    # dev: project root
        Path.cwd() / "snap",                     # cwd fallback
    ]
    for p in candidates:
        if (p / "index.html").exists():
            return str(p)
    raise FileNotFoundError(
        "snap/ directory not found. Reinstall surfy or run from the project root."
    )


def serve_and_wait(autoplay: bool = False) -> bool:
    """Start a local server, open the snap animation in browser, wait for snap.

    Parameters
    ----------
    autoplay : bool
        If True, the animation auto-triggers (used after webcam snap detection).

    Returns True if the user snapped, False if interrupted.
    """
    snap_dir = _find_snap_dir()
    handler = partial(_SnapHandler, directory=snap_dir)
    server = http.server.HTTPServer(("127.0.0.1", 0), handler)
    server.snap_event = threading.Event()

    port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    # Match the IPv4 address the server is bound to. Using "localhost" can make
    # Safari try ::1 first and wait for that connection to fail before retrying.
    url = f"http://127.0.0.1:{port}/index.html"
    if autoplay:
        url += "?autoplay=1"
    webbrowser.open(url)

    try:
        server.snap_event.wait()
        return True
    except KeyboardInterrupt:
        return False
    finally:
        server.shutdown()
