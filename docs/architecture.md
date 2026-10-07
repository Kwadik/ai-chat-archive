# AI Chat Archive — Architecture

## 1. Purpose

AI Chat Archive is a local-first application for storing, searching and viewing conversations with AI providers.

The initial provider is ChatGPT. The architecture is provider-independent so that additional providers can be added later.

The primary goals are:

* store conversations locally;
* preserve message content as Markdown;
* keep filesystem data human-readable;
* make the archive Git-friendly;
* support metadata and full-text search;
* separate provider-specific logic from storage and presentation;
* provide a local HTTP API for browser-extension integration;
* provide a read-oriented local viewer;
* support standalone offline HTML export;
* keep source files small and logically cohesive;
* make the project convenient to develop with AI assistance.

The filesystem is the source of truth.

The project intentionally avoids a database, background worker, complex synchronization infrastructure and other infrastructure that is not currently required.

---

# 2. Core Concepts

The domain hierarchy is:

```text
Project
  └── Chat
       └── Message
```

## Project

A Project groups related chats and project-level configuration.

Current fields include:

* `id`
* `name`
* `description`
* `root_path`
* `created_at`
* `updated_at`

Projects are stored under the archive root.

## Chat

A Chat represents one conversation with one AI provider.

Current fields include:

* `id`
* `provider`
* `title`
* `project_id`
* `created_at`
* `updated_at`
* `messages`
* `metadata`

A Chat is addressed by:

```text
project_id + provider + chat_id
```

The provider is part of the filesystem path and API addressing because different providers may use different identifier spaces.

## Message

A Message represents one logical user, assistant or other supported message.

Current fields include:

* `number`
* `role`
* `content`
* `file_name`
* `created_at`
* `updated_at`
* `metadata`

A Message does not require an artificial globally unique ID.

Its natural address is:

```text
project_id
  + provider
  + chat_id
  + message.number
```

This corresponds directly to the filesystem representation.

One logical Message is stored in exactly one Markdown file.

A single AI response must not be artificially split into multiple Message files merely because it contains several Markdown structures.

---

# 3. Markdown Preservation

Markdown is the primary representation of message content.

The archive preserves the Markdown received or prepared by the user as closely as possible.

Examples include:

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

The same Markdown source can be rendered for different presentation targets, including:

* the local viewer;
* standalone HTML export;
* future presentation formats.

The application must not convert stored Markdown into HTML as the primary storage format.

---

# 4. Filesystem Storage

The selected storage structure is:

```text
projects/
└── <project-id>/
    ├── project.json
    └── chats/
        └── <provider>/
            └── <chat-id>/
                ├── chat.json
                ├── 001-user.md
                ├── 002-assistant.md
                └── ...
````

## Project metadata

`project.json` contains Project metadata.

It does not contain complete chat contents.

## Chat metadata

`chat.json` contains Chat metadata, including:

* chat identity;
* provider;
* title;
* project ID;
* timestamps;
* chat metadata;
* message metadata/index information.

The actual Markdown message content remains in individual Markdown files.

## Message content

Each Message has its own Markdown file.

Example:

```text
001-user.md
002-assistant.md
003-user.md
004-assistant.md
```

Message filenames are generated when a new Message is added.

The filename is retained when an existing Message is updated, even if its role changes.

The storage layer does not renumber existing messages or recalculate their filenames.

This keeps individual files readable and makes changes Git-friendly.

---

# 5. Timestamps

All timestamps are:

* timezone-aware;
* stored as UTC;
* represented as `datetime` objects inside the domain model;
* serialized as ISO 8601 strings in JSON.

## `created_at`

`created_at` represents when the entity was originally created.

It remains unchanged when an existing entity is updated.

## `updated_at`

`updated_at` represents the most recent modification.

For a Message:

* unchanged Message → `updated_at` remains unchanged;
* changed Message → `updated_at` is updated.

For a Chat:

* unchanged Chat → `updated_at` remains unchanged;
* changed title, metadata or messages → `updated_at` is updated.

---

# 6. Storage Implementation

The filesystem storage is implemented in:

```text
chat/storage.py
```

The main class is:

```python
FileStorage
```

Current responsibilities include:

* save Project;
* load Project;
* list Projects;
* save Chat;
* load Chat;
* list Chats;
* save Message;
* search Chat metadata;
* search Message content;
* filter search by project;
* filter search by chat;
* filter search by role.

The storage layer operates directly on the filesystem.

Current exceptions include:

```python
ProjectNotFoundError
ChatNotFoundError
```

Saving a Chat requires the Project to already exist.

`save_chat()` must not silently create a missing Project.

Messages are added or updated through the Chat storage model.

---

# 7. Message Identity and Update Semantics

A Message is naturally addressed by:

```text
project_id
provider
chat_id
message.number
```

This deliberately avoids introducing an artificial `Message.id`.

## Creating a Message

When a new Message is added to a Chat:

1. the next message number is calculated;
2. a filename is generated from the number and role;
3. the Message is added to the Chat;
4. the Chat metadata is persisted;
5. the Markdown file is written.

Example:

```text
001-user.md
002-assistant.md
003-user.md
```

## Updating a Message

When a Message with an existing number is saved:

```text
existing Message
       │
       ├── unchanged
       │      └── preserve created_at and updated_at
       │
       └── changed
              ├── preserve created_at
              └── update updated_at
```

The existing Markdown filename is preserved.

Updating a Message must not create a duplicate Markdown file.

Existing orphan Markdown files are not automatically deleted.

Explicit reconciliation and deletion can be added later if a concrete requirement appears.

---

# 8. Metadata

Message and Chat metadata are stored separately from Markdown content.

Metadata can contain information such as:

* source information;
* provider-specific identifiers;
* content type;
* tags;
* language;
* attachment information;
* future provider-specific attributes.

Metadata is intended for structured filtering and integration.

The storage model does not depend on metadata being embedded into Markdown.

---

# 9. Search

Search is implemented at the storage/API layer.

The primary use case is finding something in a large archive after a long period of time.

The viewer is intentionally read-oriented and does not currently provide its own search UI.

## Message full-text search

`FileStorage.search_messages()` searches message Markdown content.

It supports optional filters:

* `project_id`;
* `chat_id`;
* `role`.

Provider is not currently exposed as a search filter.

Provider remains part of the search result context because it identifies the Chat and is useful to clients such as the browser extension.

Search is case-insensitive.

The search layer scans the filesystem-backed archive rather than maintaining a separate search index.

A database or dedicated search index may be introduced later if archive size or performance creates a concrete requirement.

The storage model should remain independent of such an optimization.

---

# 10. Search Results

Search results are represented by:

```python
SearchResult
```

A search result contains references to the original domain objects:

```text
Project
  → Chat
      → Message
```

and also exposes the provider associated with the Chat.

Conceptually:

```python
SearchResult(
    project=project,
    chat=chat,
    message=message,
    provider=chat.provider,
)
```

Search results do not create independent copies of conversation data.

The filesystem-backed domain objects remain authoritative.

---

# 11. Providers

Provider-specific browser logic is isolated from storage and the core domain model.

The browser-extension provider abstraction is intentionally small.

The current provider adapter contract is conceptually:

```typescript
interface ProviderAdapter {
    provider: string;

    canHandle(url: URL): boolean;

    getChatId(url: URL): string | null;

    getChatTitle(document: ProviderDocument): string | null;

    getChatUrl(chatId: string): string;
}
```

The current implementation includes ChatGPT.

The ChatGPT adapter is responsible for:

* recognizing `chatgpt.com`;
* extracting a ChatGPT chat ID from `/c/<chat-id>`;
* reading the current page title;
* constructing the original ChatGPT chat URL.

Provider adapters do not implement filesystem storage.

Provider adapters also do not currently scrape or import complete conversations.

The current product workflow is intentionally manual:

```text
Provider UI
    │
    │ user uses provider's Copy Markdown
    ▼
Clipboard
    │
    ▼
Extension editor
    │
    │ user cleans/edits Markdown
    ▼
Local HTTP API
```

This avoids depending on unstable provider DOM structures and keeps the initial extension focused on manual curation.

Additional providers can implement the same adapter contract later.

---

# 12. Application Layers

The current architecture is:

```text
Browser Extension
       │
       ▼
Local HTTP API
       │
       ▼
   FileStorage
       │
       ▼
   filesystem
```

The local viewer is a separate read-oriented consumer:

```text
filesystem
    │
    ▼
Viewer HTTP server
    │
    ▼
browser
```

Standalone HTML export is another derived presentation path:

```text
filesystem
    │
    ▼
Markdown rendering
    │
    ▼
standalone HTML
```

The filesystem remains the common source of truth.

---

# 13. Local HTTP API

A local HTTP API is implemented using Python's standard HTTP server infrastructure.

The API operates on `FileStorage`.

It does not introduce another source of truth.

Current operations include:

```text
GET  /projects
```

Lists projects.

```text
POST /projects
```

Creates a project.

Chat operations use:

```text
/projects/<project-id>/chats/<provider>/<chat-id>
```

Message creation:

```text
POST /projects/<project-id>/chats/<provider>/<chat-id>/messages
```

Message update:

```text
PUT /projects/<project-id>/chats/<provider>/<chat-id>/messages/<number>
```

Search:

```text
GET /search
```

The search API exposes the storage-layer message search functionality.

The exact HTTP API is intentionally thin.

Business and persistence behavior belongs in the application/storage layers rather than being duplicated in HTTP handlers.

---

# 14. Python API Client

The Python-side API client provides programmatic access to the local HTTP API.

The browser extension has its own TypeScript API client because it runs in the browser environment.

The Python and TypeScript clients communicate with the same local HTTP API.

This keeps the HTTP protocol independent from either client implementation.

---

# 15. Chrome Extension

The browser extension lives in:

```text
extension/
```

It is a separate TypeScript subproject inside the same repository.

The extension is currently focused on manual capture and navigation rather than automatic full-conversation scraping.

The current workflow is:

```text
1. User opens an AI provider chat.
2. Extension determines provider and chat context.
3. User uses the provider's own Copy Markdown action.
4. Extension reads the clipboard when available.
5. Extension opens a Markdown editor.
6. User cleans or edits the Markdown.
7. User explicitly saves.
8. Extension sends the Markdown through the local HTTP API.
```

If browser clipboard access is unavailable, the editor can still be opened and Markdown can be entered or pasted manually.

## Extension responsibilities

The extension currently handles:

* provider detection;
* chat ID detection;
* chat title detection;
* original provider chat URL generation;
* clipboard access;
* Markdown editing;
* extension UI;
* selected project configuration;
* browser storage;
* communication with the local HTTP API.

The extension does not write directly to the archive filesystem.

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

# 16. Extension UI Isolation

Extension UI is isolated from the provider page using Shadow DOM.

The extension creates its own root and panel rather than injecting application styles directly into the provider page.

The extension UI currently contains:

* extension root;
* panel;
* Markdown editor;
* Save action;
* Cancel action;
* clipboard-based editor opening.

Provider logic and application logic remain separate from the UI implementation.

The Shadow DOM is an isolation mechanism for the extension UI; it is not part of the storage or domain architecture.

---

# 17. Extension Project Configuration

The extension stores the selected Project ID in browser extension storage.

The current storage mechanism is:

```text
chrome.storage.local
```

The selected project defaults to:

```text
default
```

Conceptually:

```text
Extension
   │
   ▼
chrome.storage.local
   │
   └── selectedProjectId
```

The archive itself remains filesystem-backed.

Browser storage only contains extension configuration and does not contain archived conversation content.

The manifest requests the required Chrome permission:

```json
"permissions": [
    "storage"
]
```

---

# 18. Viewer

The viewer is a read-oriented presentation layer.

It:

* reads stored data;
* renders Markdown;
* displays projects;
* displays chats;
* displays conversations;
* provides navigation;
* supports table-of-contents presentation where appropriate;
* provides presentation controls;
* does not own the data model;
* does not become the source of truth.

The viewer currently does not implement message editing.

The viewer also intentionally does not implement full-text search.

Search is available through the storage/API layer and is intended to become primarily useful to future clients such as the browser extension.

---

# 19. Markdown Rendering

Markdown rendering is an explicit presentation-layer responsibility.

The current implementation uses a Markdown rendering library in the viewer layer.

The renderer supports the Markdown structures required by the archive, including:

* headings;
* paragraphs;
* lists;
* links;
* tables;
* fenced code blocks;
* language information for code blocks.

The specific Markdown library is an implementation detail.

It must not leak into:

* domain models;
* storage;
* API data models.

The Markdown source remains unchanged during rendering.

---

# 20. Code Blocks

Code blocks are rendered as structured HTML.

The current viewer supports syntax highlighting using Pygments.

The viewer also provides client-side functionality for copying code block contents.

These features operate on the rendered representation.

They must not modify the stored Markdown.

The Markdown file remains the source of truth.

---

# 21. Standalone HTML Export

Standalone HTML export is implemented.

The purpose is to produce a completely offline representation of stored content.

The exported file does not require:

* the Python application;
* the local HTTP server;
* the archive filesystem;
* the browser extension;
* external runtime services.

The preferred output is a single self-contained `.html` file.

Required presentation assets are embedded or otherwise included locally in the generated document.

The export is a derived representation of stored Markdown.

The Markdown files remain authoritative.

Standalone export reuses the Markdown rendering layer where practical but remains independent from the viewer's HTTP routes and filesystem layout.

---

# 22. Templates, CSS and JavaScript

The UI is separated from Python application logic.

The intended structure is:

```text
templates/
└── ...

static/
├── css/
│   └── ...
└── js/
    └── ...
```

Python modules should not become large files containing HTML, CSS and JavaScript strings.

The exact number and names of assets may evolve as the viewer grows.

The important architectural boundary is that presentation assets remain separate from storage and domain logic.

---

# 23. Tests

The project uses automated tests as an architectural protection mechanism.

Python tests live in:

```text
tests/
```

The extension has its own test suite under:

```text
extension/tests/
```

Python tests cover the domain, storage, API, API client and viewer behavior.

The extension tests cover, among other things:

* provider URL handling;
* provider adapters;
* chat context;
* clipboard behavior;
* extension UI;
* browser runtime;
* API client;
* saving messages;
* browser storage;
* project configuration;
* content-script initialization;
* manifest requirements.

The exact test count is intentionally not treated as an architectural requirement because the suite changes as functionality evolves.

Tests are run from the appropriate project directory.

Python:

```powershell
python -m pytest -v
```

Extension:

```powershell
npm test
```

A focused test is run immediately after an individual change.

After a coherent sequence of changes is complete, the relevant full suite is run.

A `FAILED` or `ERROR` result must be investigated before proceeding.

---

# 24. Development Workflow

Development follows a small-step TDD workflow:

```text
1. Define one small behavior
2. Write or update a focused test
3. Implement the behavior
4. Run the focused test
5. Investigate and fix failures
6. Run the relevant full suite after a coherent sequence
7. Continue only when green
```

The workflow deliberately avoids making several unrelated architectural changes at once.

For Python:

```powershell
python -m pytest -v
```

For the extension:

```powershell
npm test
```

The development process favors small, independently verifiable increments.

---

# 25. Local-First Principles

The project follows these principles:

1. The filesystem is the source of truth.
2. Markdown is the primary human-readable message representation.
3. JSON stores metadata and structured indexes.
4. The viewer does not own the data.
5. The browser extension does not own the data.
6. Provider-specific logic is isolated.
7. Cloud storage is not required.
8. Git should work naturally with the archive.
9. Search can evolve independently from storage.
10. Browser storage contains extension configuration, not archive content.
11. Derived HTML must never replace Markdown as the authoritative representation.
12. Small cohesive source files are preferred.
13. Avoid premature infrastructure and unnecessary abstractions.

---

# 26. Important Constraints

## One logical Message = one Markdown file

Do not split one logical AI response into multiple artificial Message objects merely because it contains:

* text;
* code;
* tables;
* lists;
* multiple paragraphs.

All of that remains one Markdown document when it represents one logical message.

## Message filenames are stable

Updating a Message must preserve its existing filename.

The storage layer does not renumber existing Messages or rename files merely because a role or other property changes.

## Viewer is read-oriented

The viewer renders stored data.

It is not the primary editing or storage system.

## Extension is manually curated

The extension does not currently attempt to scrape the entire provider conversation.

The user explicitly chooses what to capture, normally through the provider's own Copy Markdown functionality, and can edit the Markdown before saving.

## Filesystem remains authoritative

Adding a database, search index or cache in the future must not make it the authoritative copy of the conversation.

## Search is not a viewer responsibility

Search is provided through storage/API infrastructure.

The viewer remains primarily a reading and navigation interface.

## Avoid premature complexity

Do not introduce:

* a database;
* a message queue;
* a background worker;
* complex dependency injection;
* automatic full-conversation scraping;
* automatic synchronization;
* a dedicated search index;

until a concrete requirement justifies the additional complexity.

---

# 27. Current Project State

The following functionality is currently implemented.

## Backend / domain

```text
Project model
Chat model
Message model
ChatSummary model
SearchResult model
UTC timezone-aware timestamps
Message creation/update semantics
Stable message filenames
```

## Filesystem storage

```text
Project save/load/list
Chat save/load/list
Message save/update
JSON metadata
Markdown message storage
Metadata filtering
Full-text message search
SearchResult generation
```

## HTTP API

```text
Project listing
Project creation
Chat access
Message creation
Message update
Message metadata
Full-text search
```

## Python API client

```text
Project access
Chat access
Message creation
Message update
```

## Viewer

```text
Jinja2 templates
Markdown rendering
Syntax highlighting
Code copy functionality
Project listing
Chat listing
Chat viewing
Navigation
Standalone HTML export
Separate CSS
Separate JavaScript
```

## Browser extension

```text
TypeScript extension project
Manifest V3
ChatGPT provider adapter
Provider/chat context detection
Chat URL generation
Clipboard reading
Markdown editor
Shadow DOM UI
Browser runtime
Local API client
Message saving
Selected project configuration
chrome.storage.local
Chrome storage permission
```

## Testing

The Python and extension layers have dedicated automated test suites.

The extension suite currently covers 28 test files and 97 tests.

The test suite is expected to grow as functionality is added.

---

# 28. Current Extension Boundaries

The browser extension is intentionally limited to the following responsibilities:

```text
Provider page
     │
     ├── identify provider
     ├── identify chat
     ├── identify title
     │
     ▼
User chooses/copies content
     │
     ▼
Clipboard
     │
     ▼
Markdown editor
     │
     ▼
Local HTTP API
```

The extension does not currently:

* parse the complete provider DOM;
* automatically import every message;
* maintain an independent conversation database;
* write directly to the filesystem;
* synchronize conversations in the background;
* provide a separate search index.

These are deferred until concrete requirements appear.

---

# 29. Future Development Direction

The next features should be implemented incrementally.

Likely areas include:

```text
Extension project selection UI
Project management through the extension
Chat navigation from search results
Additional provider adapters
Improved chat-title observation
Additional API operations where required
```

Potential future work includes:

```text
Automatic conversation import
Additional providers
Advanced search/indexing
Attachments
More extension settings
Optional synchronization features
```

These features should be introduced only when their concrete behavior is understood and can be protected with focused tests.

The architecture should continue to prefer:

```text
small behavior
→ focused test
→ implementation
→ focused green test
→ coherent full-suite verification
```

over large speculative subsystems.
