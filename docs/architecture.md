# AI Chat Archive — Architecture

## 1. Purpose

AI Chat Archive is a local-first application for storing and viewing conversations with AI providers.

The initial target provider is ChatGPT. The architecture is intentionally provider-independent so that Claude, Gemini, and other providers can be added later.

The primary goals are:

* store conversations locally;
* preserve message content as original Markdown;
* keep filesystem data human-readable;
* make the archive Git-friendly;
* allow searching and filtering by metadata;
* separate provider-specific logic from storage and UI;
* support future browser-extension integration through a local HTTP API;
* keep source files small and logically cohesive;
* make the project convenient to develop with AI assistance.

The filesystem is the source of truth.

---

# 2. Core Concepts

The domain hierarchy is:

```text
Project
  └── Chat
       └── Message
```

## Project

A Project groups related chats and project-level files.

Current fields:

* `id`
* `name`
* `description`
* `root_path`
* `created_at`
* `updated_at`

## Chat

A Chat represents one conversation with one AI provider.

Current fields:

* `id`
* `provider`
* `title`
* `project_id`
* `created_at`
* `updated_at`
* `messages`
* `metadata`

## Message

A Message represents one logical user or assistant message.

Current fields:

* `number`
* `role`
* `content`
* `file_name`
* `created_at`
* `updated_at`
* `metadata`

One logical Message is stored in exactly one Markdown file.

A single AI response must not be artificially split into multiple Message files.

---

# 3. Markdown Preservation

Markdown is the primary representation of message content.

The archive must preserve the Markdown received from the provider as closely as possible.

Examples:

````markdown
# Heading

Some text.

- item one
- item two

```python
print("hello")
````

````

Tables, lists, code blocks, headings, links and other Markdown structures remain Markdown in storage.

The viewer renders Markdown but does not become the source of truth.

Rendered HTML is a derived representation of Markdown.

HTML must not be stored as the authoritative representation of a Message.

The same Markdown source may be rendered for different presentation targets, including:

* the local viewer;
* standalone HTML export;
* future other presentation formats.

The application must not convert stored Markdown into HTML as the primary storage format.

---

# 4. Filesystem Storage

The selected storage structure is:

```text
projects/
└── <project-id>/
    ├── project.json
    └── chats/
        ├── chatgpt/
        │   └── <chat-id>/
        │       ├── chat.json
        │       ├── 001-user.md
        │       ├── 002-assistant.md
        │       └── ...
        └── claude/
            └── <chat-id>/
                ├── chat.json
                └── ...
````

## Project metadata

`project.json` contains Project metadata.

It does not contain the complete chat contents.

## Chat metadata

`chat.json` contains:

* chat identity;
* provider;
* title;
* project ID;
* timestamps;
* chat metadata;
* message metadata/index.

It does not contain the actual Markdown message contents.

## Message content

Each Message has its own Markdown file.

Example:

```text
001-user.md
002-assistant.md
003-user.md
004-assistant.md
```

This keeps individual files small, readable and Git-friendly.

---

# 5. Timestamps

All timestamps are:

* timezone-aware;
* stored as UTC;
* represented as `datetime` objects inside the domain model;
* serialized as ISO 8601 strings in JSON.

## created_at

`created_at` represents when the entity was originally created.

It must remain unchanged when an existing entity is updated.

## updated_at

`updated_at` represents the most recent modification.

For a Message:

* unchanged Message → `updated_at` remains unchanged;
* changed Message → `updated_at` is updated.

For a Chat:

* unchanged Chat → `updated_at` remains unchanged;
* changed title, metadata or messages → `updated_at` is updated.

---

# 6. Current Storage Implementation

The current filesystem storage is implemented in:

```text
chat/storage.py
```

The main class is:

```python
FileStorage
```

Current responsibilities:

* save Project;
* load Project;
* list Projects;
* save Chat;
* load Chat;
* search Chat metadata.

Current exceptions:

```python
ProjectNotFoundError
ChatNotFoundError
```

Saving a Chat requires the Project to already exist.

`save_chat()` must not silently create a missing Project.

---

# 7. Message Update Semantics

When saving an existing Chat:

```text
existing Message
       │
       ├── same content/metadata
       │       └── preserve created_at and updated_at
       │
       └── changed content/metadata
               ├── preserve created_at
               └── update updated_at
```

The Markdown file is updated in place.

Updating a Message must not create duplicate Markdown files.

Existing orphan Markdown files are currently not automatically deleted.

Explicit reconciliation/deletion can be added later.

---

# 8. Metadata and Search

Message metadata exists separately from Markdown content.

The purpose of metadata is to support:

* date filtering;
* project filtering;
* provider filtering;
* chat filtering;
* role filtering;
* future tags;
* future content types;
* provider-specific identifiers;
* future attachments;
* future language information.

The current storage layer can scan JSON metadata without using Markdown as the filtering criterion.

Full-text search is a separate future concern.

Possible future implementations include:

* SQLite index;
* SQLite FTS;
* another local search index.

The storage model should not need to change when full-text search is introduced.

---

# 9. Search Results

Search should conceptually return references to source data rather than create independent copies of conversations.

A search result should be able to identify:

```text
Project
  → Provider
      → Chat
          → Message
```

The exact search-result model can be introduced later.

---

# 10. Providers

Provider-specific logic is isolated behind services.

Conceptually:

```text
AIService
  ├── ChatGPTService
  ├── ClaudeService
  └── GeminiService
```

Base interface:

```python
class AIService(ABC):
    name = "unknown"

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        ...

    @abstractmethod
    def get_chat_id(self, url: str) -> str:
        ...

    @abstractmethod
    def get_chat_title(self) -> str:
        ...

    @abstractmethod
    def get_messages(self) -> list[Any]:
        ...
```

Provider services are responsible for understanding provider-specific pages/data.

They should not contain filesystem storage implementation.

---

# 11. Application Layers

The intended architecture is:

```text
Browser Extension ─────┐
                       │
                       ▼
                 Local HTTP API
                       │
                       ▼
                   FileStorage
                       │
                       ▼
                   filesystem


Local Viewer ──────────► stored data / viewer HTTP server
```

The viewer is a separate consumer of the stored data.

---

# 12. Future Local HTTP API

The future API is expected to expose operations conceptually similar to:

```text
GET  /api/projects
POST /api/projects

GET  /api/chats/<provider>/<chat_id>
POST /api/chats/<provider>/<chat_id>/sync

PUT  /api/chats/<provider>/<chat_id>/title

POST /api/chats/<provider>/<chat_id>/messages

GET  /api/search?...
```

The exact API is not implemented yet.

The API must operate on the filesystem storage layer rather than introducing a second source of truth.

---

# 13. Chrome Extension

The future Chrome Extension will provide a convenient way to save information from AI websites.

Expected capabilities:

* floating save button/panel;
* save user message;
* save assistant message;
* save both;
* determine provider;
* determine chat ID;
* determine chat title;
* select Project;
* send Markdown to the local Python server;
* optionally synchronize a complete chat;
* project/settings management;
* potentially automatic saving.

The extension must not write directly to the archive filesystem.

Instead:

```text
Chrome Extension
       │
       ▼
localhost HTTP API
       │
       ▼
Python application
       │
       ▼
FileStorage
       │
       ▼
filesystem
```

---

# 14. Viewer

The viewer is a presentation layer.

It must:

* read stored Markdown;
* render Markdown;
* display conversations;
* provide navigation;
* provide table of contents where appropriate;
* support dark/light presentation as implemented;
* avoid modifying the source archive.

The viewer does not own the data model.

The viewer must not become the source of truth.

## Markdown rendering

Markdown rendering is an explicit presentation-layer responsibility.

The Markdown renderer should support:

* standard Markdown structures;
* headings;
* paragraphs;
* lists;
* links;
* tables where supported;
* fenced code blocks;
* language information for code blocks.

The renderer should be isolated from the viewer templates so that the same Markdown-to-HTML rendering logic can be reused by other presentation targets.

The specific Markdown library is an implementation detail and should not leak into storage or domain models.

## Code blocks

Code blocks are rendered as structured HTML.

Future presentation features may include:

* syntax highlighting;
* language-specific styling;
* copying code block contents.

These features must operate on the rendered representation and must not modify the stored Markdown.

## Editing

The initial viewer is read-oriented.

Message editing is not part of the initial viewer implementation.

A future browser extension may provide a Markdown editor before saving content through the local HTTP API.

The viewer may reuse editor components in the future, but the editor is not currently part of the viewer architecture.

---

# 15. Standalone HTML Export

The application should eventually support exporting a Chat as a standalone HTML file.

The exported file must be viewable without:

* the Python application;
* the local HTTP server;
* the archive filesystem;
* the browser extension;
* external runtime services.

The preferred output is a single self-contained `.html` file.

The standalone document should contain all required presentation assets locally, including CSS and JavaScript required for the exported functionality.

The exported HTML is a derived representation of the stored Markdown.

The Markdown files remain the source of truth and must not be replaced by exported HTML.

Standalone export should reuse the same Markdown rendering layer as the local viewer where practical.

The export format should remain independent from the local viewer's HTTP routes and filesystem layout.

---

# 16. Templates, CSS and JavaScript

The UI should not be implemented as one large Python file containing HTML/CSS/JavaScript strings.

The intended structure is:

```text
templates/
└── index.html

static/
├── css/
│   ├── base.css
│   ├── viewer.css
│   └── toc.css
└── js/
    ├── viewer.js
    ├── toc.js
    └── reload.js
```

Python modules should remain small and logically cohesive.

This is important because individual files should be easy to inspect, modify and provide to an AI assistant.

---

# 17. Tests

Tests live in:

```text
tests/
```

Current test files:

```text
tests/
├── test_models.py
└── test_storage.py
```

Tests are run from the project root with:

```powershell
python -m pytest -v
```

Do not rely on the standalone `pytest` executable being available in PATH.

Current tests cover:

* Message defaults;
* Chat defaults;
* Project defaults;
* custom Message filename;
* Project save/load;
* missing Project;
* Chat save/load;
* expected filesystem structure;
* saving Chat with missing Project;
* Message timestamp update semantics;
* unchanged Message timestamp preservation;
* avoiding duplicate Markdown files.

Tests are part of the architecture protection, not only final validation.

---

# 18. Development Workflow

Development follows a small-step test-driven workflow:

```text
1. Define one small behavior
2. Write/update a test
3. Implement the behavior
4. Run the full test suite
5. Fix failures
6. Continue only when green
```

The normal validation command is:

```powershell
python -m pytest -v
```

Expected successful result:

```text
X passed
```

A `FAILED` result must be investigated before proceeding.

An `ERROR` result must also be investigated before proceeding.

---

# 19. Local-First Principles

The project follows these principles:

1. Filesystem is the source of truth.
2. Markdown is the primary human-readable message representation.
3. JSON stores metadata and indexes.
4. The viewer does not own the data.
5. Provider-specific logic is isolated.
6. Cloud storage is not required.
7. Git should work naturally with the archive.
8. Search/indexing can evolve independently from storage.
9. Small cohesive source files are preferred.
10. Avoid premature infrastructure and unnecessary abstractions.

---

# 20. Important Constraints

The following constraints are architectural requirements.

### One logical Message = one Markdown file

Do not split one AI response into multiple artificial Message objects merely because it contains:

* text;
* code;
* tables;
* lists;
* multiple paragraphs.

All of that remains one Markdown document when it represents one logical message.

### Viewer is read-oriented

The viewer renders stored data.

It is not the primary editing/storage system.

### Filesystem remains authoritative

Adding a database, search index or cache in the future must not make it the authoritative copy of the conversation.

### Avoid premature complexity

Do not introduce a database, message queue, background worker, complex dependency injection framework or other infrastructure until a concrete requirement exists.

---

# 21. Current Project State

Implemented:

```text
Project model
Chat model
Message model
ChatSummary model
Filesystem storage
JSON metadata
Markdown message storage
UTC timestamps
Project loading/saving
Chat loading/saving
Chat listing
Metadata filtering foundation
Local HTTP API
HTTP client
Jinja2-based viewer
Separate CSS
Separate JavaScript
Project listing page
Project chat listing
Chat viewing page
```

Partially implemented / currently under development:

```text
Markdown-to-HTML rendering
Viewer presentation
Code block rendering
```

Not implemented yet:

```text
Standalone HTML export
Syntax highlighting
Copy buttons for code blocks
Full-text search
Search result model
Provider implementations
ChatGPT integration
Synchronization logic
Chrome Extension
Extension Markdown editor
Viewer message editing
```

The next development steps should continue incrementally from the existing tested storage, API and viewer layers.

