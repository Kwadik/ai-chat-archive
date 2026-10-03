import viewer.renderer as renderer

from chat.models import Project
from viewer.renderer import TEMPLATES_DIR, render_project


def test_project_template_exists():
    template_path = TEMPLATES_DIR / "project.html"

    assert template_path.is_file()


def test_render_project():
    project = Project(
        id="project-1",
        name="My Project",
        description="Test project",
        root_path="/projects/my-project",
    )

    html = render_project(project)

    assert "My Project" in html
    assert "Test project" in html


def test_render_projects():
    projects = [
        Project(
            id="project-1",
            name="First Project",
        ),
        Project(
            id="project-2",
            name="Second Project",
        ),
    ]

    html = renderer.render_projects(projects)

    assert "First Project" in html
    assert "Second Project" in html

def test_project_template_references_static_assets():
    project = Project(
        id="project-1",
        name="My Project",
    )

    html = render_project(project)

    assert '/static/css/viewer.css' in html
    assert '/static/js/viewer.js' in html

def test_render_chat():
    from chat.models import Chat, Message
    from viewer.renderer import render_chat

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Hello, viewer!",
            ),
        ],
    )

    html = render_chat(chat)

    assert "My First Chat" in html
    assert "Hello, viewer!" in html

def test_render_chat_renders_markdown_heading():
    from chat.models import Chat, Message
    from viewer.renderer import render_chat

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content="# Hello",
            ),
        ],
    )

    html = render_chat(chat)

    assert "<h1>Hello</h1>" in html

def test_render_chat_renders_code_block():
    from chat.models import Chat, Message
    from viewer.renderer import render_chat

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content='```python\nprint("hello")\n```',
            ),
        ],
    )

    html = render_chat(chat)

    assert '<code class="language-python">' in html
    assert '<span class="nb">print</span>' in html
    assert '<span class="s2">"hello"</span>' in html

def test_render_chat_renders_javascript_code_block():
    from chat.models import Chat, Message
    from viewer.renderer import render_chat

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content='```javascript\nconsole.log("hello");\n```',
            ),
        ],
    )

    html = render_chat(chat)

    assert '<code class="language-javascript">' in html
    assert '<span class="nx">console</span>' in html
    assert '<span class="nx">log</span>' in html
    assert '<span class="s2">"hello"</span>' in html

def test_render_chat_highlights_python_code():
    from chat.models import Chat, Message
    from viewer.renderer import render_chat

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content='```python\nprint("hello")\n```',
            ),
        ],
    )

    html = render_chat(chat)

    assert '<code class="language-python">' in html
    assert "<span" in html

def test_viewer_css_contains_pygments_styles():
    from pathlib import Path

    css_path = Path("viewer/static/css/viewer.css")

    css = css_path.read_text(encoding="utf-8")

    assert ".nb" in css
    assert ".s2" in css

def test_render_chat_renders_unknown_code_language():
    from chat.models import Chat, Message
    from viewer.renderer import render_chat

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content='```unknown-language\nhello("world")\n```',
            ),
        ],
    )

    html = render_chat(chat)

    assert '<code class="language-unknown-language">' in html
    assert 'hello(&quot;world&quot;)' in html

def test_render_chat_renders_code_block_without_language():
    from chat.models import Chat, Message
    from viewer.renderer import render_chat

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content='```\nprint("hello")\n```',
            ),
        ],
    )

    html = render_chat(chat)

    assert "<pre><code>" in html
    assert 'class="language-"' not in html
    assert "print(&quot;hello&quot;)" in html

def test_render_chat_preserves_multiline_code_block():
    from chat.models import Chat, Message
    from viewer.renderer import render_chat

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content='```python\nfirst = 1\nsecond = 2\nprint(first + second)\n```',
            ),
        ],
    )

    html = render_chat(chat)

    assert "first" in html
    assert "second" in html
    assert "print" in html
    assert "\n" in html

def test_viewer_css_contains_pygments_token_styles():
    from pathlib import Path

    css_path = Path("viewer/static/css/viewer.css")
    css = css_path.read_text(encoding="utf-8")

    assert ".k" in css
    assert ".nf" in css
    assert ".o" in css

def test_render_chat_renders_copy_button_for_code_block():
    from chat.models import Chat, Message
    from viewer.renderer import render_chat

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content='```python\nprint("hello")\n```',
            ),
        ],
    )

    html = render_chat(chat)

    assert 'class="copy-code-button"' in html
    assert "Copy code" in html


def test_viewer_js_copy_code_behavior():
    from pathlib import Path

    js_path = Path("viewer/static/js/viewer.js")
    js = js_path.read_text(encoding="utf-8")

    # Find the copy button and its code block.
    assert 'closest(".copy-code-button")' in js
    assert 'button.parentElement.querySelector("code")' in js

    # Copy the actual code text.
    assert "navigator.clipboard.writeText(code.innerText)" in js

    # Show temporary success feedback.
    assert 'button.classList.add("copied")' in js
    assert 'button.textContent = "Copied!"' in js
    assert "setTimeout" in js
    assert 'button.textContent = "Copy code"' in js
    assert 'button.classList.remove("copied")' in js

    # Handle clipboard failure.
    assert ".catch" in js
    assert 'button.textContent = "Copy failed"' in js

def test_export_chat_html_returns_standalone_document():
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Hello, viewer!",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert "<!DOCTYPE html>" in html
    assert "<title>My First Chat</title>" in html
    assert "Hello, viewer!" in html