from __future__ import annotations
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

from chat.storage import (
    ChatNotFoundError,
    FileStorage,
    ProjectNotFoundError,
)
from viewer.renderer import (
    render_chat,
    render_project,
    render_projects,
)


STATIC_DIR = Path(__file__).parent / "static"

class ViewerRequestHandler(BaseHTTPRequestHandler):
    storage: FileStorage

    def do_GET(self) -> None:
        if self.path == "/":
            projects = self.storage.list_projects()
            html = render_projects(projects)

            self._send_html(html, 200)
            return

        if self.path.startswith("/projects/") and "/chats/" in self.path:
            parts = self.path.strip("/").split("/")

            project_id = parts[1]
            provider = parts[3]
            chat_id = parts[4]

            try:
                chat = self.storage.load_chat(
                    project_id,
                    provider,
                    chat_id,
                )
            except ChatNotFoundError:
                self.send_response(404)
                self.end_headers()
                return

            html = render_chat(chat)
            self._send_html(html, 200)
            return

        if self.path.startswith("/projects/"):
            project_id = self.path.removeprefix("/projects/")

            try:
                project = self.storage.load_project(project_id)
            except ProjectNotFoundError:
                self.send_response(404)
                self.end_headers()
                return

            chats = self.storage.list_chats(project_id)
            html = render_project(project, chats)

            self._send_html(html, 200)
            return

        if self.path == "/static/css/viewer.css":
            css_path = STATIC_DIR / "css" / "viewer.css"
            body = css_path.read_bytes()

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/css; charset=utf-8",
            )
            self.send_header(
                "Content-Length",
                str(len(body)),
            )
            self.end_headers()

            self.wfile.write(body)
            return

        if self.path == "/static/js/viewer.js":
            js_path = STATIC_DIR / "js" / "viewer.js"
            body = js_path.read_bytes()

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/javascript; charset=utf-8",
            )
            self.send_header(
                "Content-Length",
                str(len(body)),
            )
            self.end_headers()

            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        pass

    def _send_html(self, html: str, status: int) -> None:
        body = html.encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(body)),
        )
        self.end_headers()

        self.wfile.write(body)


def create_server(
    storage: FileStorage,
    *,
    host: str = "127.0.0.1",
    port: int = 0,
) -> HTTPServer:
    handler = type(
        "ConfiguredViewerRequestHandler",
        (ViewerRequestHandler,),
        {"storage": storage},
    )

    return HTTPServer(
        (host, port),
        handler,
    )