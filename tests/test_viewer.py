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

def test_export_chat_html_uses_standalone_template():
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
                content="Hello, standalone!",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert "<!DOCTYPE html>" in html
    assert "<title>My First Chat</title>" in html
    assert "<main>" in html
    assert "Hello, standalone!" in html

def test_standalone_template_exists():
    template_path = TEMPLATES_DIR / "standalone.html"

    assert template_path.is_file()

def test_export_chat_html_contains_css():
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
                role="assistant",
                content="Hello!",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert "<style>" in html
    assert ".nb" in html

def test_export_chat_html_has_no_external_static_dependencies():
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
                role="assistant",
                content="Hello!",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert "/static/css/" not in html
    assert "/static/js/" not in html

def test_export_chat_html_contains_copy_code_js():
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
                role="assistant",
                content="```python\nprint('hello')\n```",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert "navigator.clipboard.writeText(code.innerText)" in html

def test_export_chat_html_has_no_external_asset_references():
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
                role="assistant",
                content="Hello!",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert '<link rel="stylesheet"' not in html
    assert '<script src=' not in html

def test_export_chat_html_contains_copy_button():
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
                role="assistant",
                content="```python\nprint('hello')\n```",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert 'class="copy-code-button"' in html
    assert "Copy code" in html

def test_export_chat_html_is_standalone_document():
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
                content="# Hello\n\nThis is my chat.",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert "<!DOCTYPE html>" in html
    assert "<html" in html
    assert "<head>" in html
    assert "<body>" in html
    assert "<h1>My First Chat</h1>" in html
    assert "<h1>Hello</h1>" in html
    assert "This is my chat." in html

def test_export_chat_html_file_writes_html(tmp_path):
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html_file

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My First Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="# Hello",
            ),
        ],
    )

    output_path = tmp_path / "chat.html"

    export_chat_html_file(chat, output_path)

    assert output_path.exists()

    html = output_path.read_text(encoding="utf-8")

    assert "<!DOCTYPE html>" in html
    assert "<h1>My First Chat</h1>" in html
    assert "<h1>Hello</h1>" in html

def test_export_chat_html_file_overwrites_existing_file(tmp_path):
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html_file

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Updated Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="New content",
            ),
        ],
    )

    output_path = tmp_path / "chat.html"
    output_path.write_text("old content", encoding="utf-8")

    export_chat_html_file(chat, output_path)

    html = output_path.read_text(encoding="utf-8")

    assert "old content" not in html
    assert "Updated Chat" in html
    assert "New content" in html

def test_export_chat_html_file_writes_utf8(tmp_path):
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html_file

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Русский чат 🚀",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Привет, мир! 🌍",
            ),
        ],
    )

    output_path = tmp_path / "chat.html"

    export_chat_html_file(chat, output_path)

    html = output_path.read_text(encoding="utf-8")

    assert "Русский чат 🚀" in html
    assert "Привет, мир! 🌍" in html

def test_export_chat_html_file_contains_no_external_resources(tmp_path):
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html_file

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content="Hello!",
            ),
        ],
    )

    output_path = tmp_path / "chat.html"

    export_chat_html_file(chat, output_path)

    html = output_path.read_text(encoding="utf-8")

    assert 'href="http://' not in html
    assert 'href="https://' not in html
    assert 'src="http://' not in html
    assert 'src="https://' not in html

def test_export_chat_html_file_contains_all_messages_in_order(tmp_path):
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html_file

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Conversation",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="First message",
            ),
            Message(
                number=2,
                role="assistant",
                content="Second message",
            ),
            Message(
                number=3,
                role="user",
                content="Third message",
            ),
        ],
    )

    output_path = tmp_path / "chat.html"

    export_chat_html_file(chat, output_path)

    html = output_path.read_text(encoding="utf-8")

    first = html.index("First message")
    second = html.index("Second message")
    third = html.index("Third message")

    assert first < second < third

def test_export_chat_html_file_returns_output_path(tmp_path):
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html_file

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="My Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Hello!",
            ),
        ],
    )

    output_path = tmp_path / "chat.html"

    result = export_chat_html_file(chat, output_path)

    assert result == output_path

def test_export_chat_html_escapes_chat_title(tmp_path):
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title='Chat <Test> & "Demo"',
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="user",
                content="Hello!",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert "<title>Chat &lt;Test&gt; &amp; &#34;Demo&#34;</title>" in html
    assert "<title>Chat <Test>" not in html

def test_export_chat_html_contains_syntax_highlighting():
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Code Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content="```python\nprint('hello')\n```",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert '<code class="language-python">' in html
    assert '<span class="nb">print</span>' in html

def test_export_chat_html_preserves_code_text_for_copy():
    from chat.models import Chat, Message
    from viewer.renderer import export_chat_html

    chat = Chat(
        id="chat-1",
        provider="chatgpt",
        title="Code Chat",
        project_id="project-1",
        messages=[
            Message(
                number=1,
                role="assistant",
                content="```python\nprint('hello')\nreturn 42\n```",
            ),
        ],
    )

    html = export_chat_html(chat)

    assert '<code class="language-python">' in html
    assert '<span class="nb">print</span>' in html
    assert "hello" in html
    assert "<span class=\"mi\">42</span>" in html