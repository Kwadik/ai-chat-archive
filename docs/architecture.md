# AI Chat Archive — Architecture

## 1. Purpose

**AI Chat Archive** is a local-first file-based archive for conversations with AI services.

The primary goals are:

- preserve AI conversations locally in Markdown;
- make conversations easy to search and inspect from an IDE;
- avoid dependence on a single AI provider;
- organize multiple AI conversations around projects;
- provide a local viewer for archived conversations;
- provide a Chrome extension for convenient capture and synchronization;
- keep the stored data human-readable and Git-friendly.

The archive is local. No cloud database is required.

---

## 2. Core Concepts

The system has three primary concepts:

```text
Project
   │
   └── Chat
         │
         └── Message
```

### Project

A user-defined workspace representing a real task, application, research topic, or other body of work.

A project may contain chats from multiple AI providers.

### Chat

A conversation imported from an AI provider.

A chat belongs to exactly one project.

A chat has:

- stable provider-specific ID;
- provider name;
- current title;
- project ID;
- ordered messages.

### Message

A single user or assistant message.

Messages are stored as Markdown files.

The original Markdown representation should be preserved whenever possible.

---

## 3. Providers

AI providers are adapters, not part of the core storage model.

Initial MVP provider:

- ChatGPT

Future providers may include:

- Claude
- Gemini
- local AI services
- other web-based AI interfaces

Provider-specific code must be isolated behind a common adapter interface.

Conceptually:

```text
Provider Adapter
       │
       ├── detect current chat
       ├── get chat ID
       ├── get chat title
       └── extract messages
```

The core application must not depend on ChatGPT-specific page structures.

---

## 4. Storage

The archive is file-based.

Markdown is the primary content format.

Example:

```text
projects/
└── ai-chat-archive/
    └── chats/
        ├── chatgpt/
        │   └── <chat-id>/
        │       ├── title.txt
        │       ├── chat.json
        │       ├── 001-user.md
        │       ├── 002-assistant.md
        │       └── ...
        └── claude/
            └── ...
```

Message files should remain ordinary Markdown files.

Do not store the complete conversation inside a large JSON document.

`chat.json` is metadata/index information only.

---

## 5. Message Metadata

Message content and message metadata are separate concerns.

The Markdown file remains the primary source of message content. Metadata is stored separately and is used for searching, filtering, indexing and navigation.

Each message should have a minimal metadata record containing at least:

```json
{
    "number": 12,
    "role": "assistant",
    "file": "012-assistant.md",
    "created_at": "2026-09-18T15:42:31Z"
}
```

The metadata model should be extensible.

Possible future metadata may include:

- `updated_at`;
- provider-specific message ID;
- parent/response relationship;
- tags;
- attachments;
- detected language;
- content type;
- other provider-specific or application-level attributes.

The message timestamp belongs to the **Message**, not only to the Chat.

Metadata should remain lightweight. It must not become a second copy of the message content.

---

## 6. Search and Filtering

Search and filtering are first-class architectural requirements.

The archive should allow users to find previously stored conversations and messages even when they no longer remember the exact chat or project in which the information was discussed.

An important use case is time-based discovery:

> "A few weeks ago I worked through something useful in one of the AI chats, but I don't remember which chat."

Therefore the architecture must support filtering by message metadata, especially by date.

Initial filtering dimensions should include:

- project;
- provider;
- chat;
- message role;
- creation date/time;
- date ranges.

The architecture should allow additional filters to be introduced later, such as:

- tags;
- content type;
- attachments;
- language;
- other metadata.

Search implementation is intentionally not prescribed by the MVP architecture.

The initial implementation may search directly through the filesystem and metadata. A dedicated search index or database may be introduced later if the archive becomes large enough to require it.

The important architectural requirement is:

> **Stored messages must contain sufficient metadata to support efficient search and filtering without requiring the system to parse every Markdown file for every query.**

Search results should reference the original Chat and Message rather than creating separate copies of message content.

---

## 7. Markdown Preservation

The archive should preserve the Markdown returned by the AI interface whenever possible.

In particular, preserve:

- fenced code blocks;
- programming-language identifiers;
- tables;
- lists;
- links;
- headings;
- blockquotes;
- inline formatting.

HTML conversion belongs to the viewer layer.

---

## 8. Project Configuration

Projects are user-managed entities.

A project should contain at least:

```text
id
name
root_path
```

The initial MVP may support a single configured project while keeping the data model capable of supporting multiple projects.

Future browser-extension settings should provide:

- create project;
- rename project;
- select project;
- change project path;
- remove project from extension configuration.

Removing a project from configuration must not automatically delete its files.

---

## 9. Components

The application consists of several independent layers.

```text
Chrome Extension
       │
       │ HTTP API
       ▼
Local Python Server
       │
       ├── Provider adapters
       ├── Chat/message storage
       └── Project configuration
       │
       ▼
Local filesystem
       │
       ├── Markdown
       ├── JSON metadata
       └── project files
       │
       ▼
Web Viewer
```

### Chrome Extension

Responsible for:

- detecting supported AI services;
- identifying the current chat;
- obtaining Markdown content;
- detecting chat title;
- selecting the target project;
- sending data to the local server.

### Local Python Server

Responsible for:

- filesystem access;
- project configuration;
- chat storage;
- local HTTP API;
- serving the viewer.

### Viewer

Responsible only for presentation.

It should not contain storage logic.

---

## 10. Templates, CSS and JavaScript

HTML must not be embedded into large Python f-strings.

Use a template engine such as **Jinja2**.

Example structure:

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

Responsibilities should remain separated:

- Python — application and data logic;
- Jinja2 — HTML structure;
- CSS — presentation;
- JavaScript — browser interaction.

This is important both for maintainability and for working with AI assistants: individual files should remain small enough to inspect and modify independently.

---

## 11. Local API

The Chrome extension communicates with the local server through HTTP.

Initial conceptual endpoints:

```text
GET  /api/projects
POST /api/projects

GET  /api/chats/<provider>/<chat_id>
POST /api/chats/<provider>/<chat_id>/sync

PUT  /api/chats/<provider>/<chat_id>/title

POST /api/chats/<provider>/<chat_id>/messages

GET  /api/search?...
```

The API is local-only and should listen on `127.0.0.1`.

The API contract should not expose provider-specific implementation details unnecessarily.

---

## 12. Local-first Principles

The project follows these principles:

1. Local files are the source of truth.
2. Markdown is the primary human-readable content format.
3. Message metadata is stored separately from message content.
4. Message metadata is designed for search, filtering and indexing.
5. No cloud database is required.
6. Provider-specific logic is isolated.
7. The viewer does not own or transform stored content.
8. Project configuration is separate from chat content.
9. Files should remain easy to inspect, search, edit and version with Git.
10. Search/indexing mechanisms may evolve without changing the underlying Markdown storage format.
11. Components should remain small enough to provide independently to an AI assistant for analysis or modification.
12. The storage model should remain extensible without requiring a migration of existing Markdown content.

---

## 13. MVP Scope

### Included

- local Python server;
- file-based storage;
- Markdown messages;
- message metadata;
- project-aware data model;
- search/filtering architecture;
- ChatGPT provider adapter;
- Chrome extension;
- chat title and ID detection;
- user/assistant message separation;
- local viewer;
- Jinja2 templates;
- separated CSS and JavaScript;
- basic project configuration.

### Not required initially

- cloud synchronization;
- database;
- authentication;
- embeddings;
- RAG;
- semantic search;
- automatic conversation analysis;
- support for every AI provider;
- complex project management UI.

The architecture should allow these features to be added later without replacing the storage model.

---

## 14. Design Principle

The system should optimize not only for software maintainability, but also for **AI-assisted development**.

A developer should be able to provide an AI assistant with a small, relevant set of files:

```text
chatgpt.py
storage.py
templates/index.html
static/js/toc.js
```

instead of an entire large application.

Therefore:

> **Small, cohesive, independently understandable files are a first-class architectural requirement.**
