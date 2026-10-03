from __future__ import annotations
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from html import escape

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from chat.models import Chat, Project

TEMPLATES_DIR = Path(__file__).parent / "templates"

_environment = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=True,
)

def get_pygments_css() -> str:
    return HtmlFormatter().get_style_defs(".highlight")

def _highlight_code(tokens, idx, options, env) -> str:
    token = tokens[idx]

    language = token.info.strip().split()[0] if token.info.strip() else ""

    if language:
        try:
            lexer = get_lexer_by_name(language)
        except ClassNotFound:
            lexer = None
    else:
        lexer = None

    if lexer is None:
        code = escape(token.content)
    else:
        code = highlight(
            token.content,
            lexer,
            HtmlFormatter(nowrap=True),
        )

    language_class = f' class="language-{escape(language)}"' if language else ""

    return (
        '<div class="code-block">'
        '<button type="button" class="copy-code-button">Copy code</button>'
        f"<pre><code{language_class}>{code}</code></pre>"
        "</div>\n"
    )


_markdown = MarkdownIt()
_markdown.renderer.rules["fence"] = _highlight_code

def render_project(
    project: Project,
    chats: list[Chat] | None = None,
) -> str:
    template = _environment.get_template("project.html")

    return template.render(
        project=project,
        chats=chats or [],
    )

def render_projects(projects: list[Project]) -> str:
    template = _environment.get_template("projects.html")

    return template.render(
        projects=projects,
    )

def render_chat(chat: Chat) -> str:
    template = _environment.get_template("chat.html")

    messages = [
        {
            "message": message,
            "html": render_markdown(message.content),
        }
        for message in chat.messages
    ]

    return template.render(
        chat=chat,
        messages=messages,
    )

def render_markdown(content: str) -> str:
    return _markdown.render(content)