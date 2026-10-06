# AI Chat Archive Extension

Browser extension for manually selecting and archiving important messages from AI chat interfaces into the local AI Chat Archive.

The extension is intentionally designed as a small, local-first capture and navigation tool. It does not attempt to automatically archive entire conversations.

## Goals

The extension should allow the user to:

- manually select an important message for archiving;
- obtain Markdown copied from the AI chat interface;
- edit the Markdown before saving;
- preview the rendered Markdown;
- save the message to the local AI Chat Archive API;
- associate the message with the current project and chat;
- detect the current provider and chat ID from the page URL;
- detect the current chat title;
- notice chat title changes;
- browse projects and chats;
- search archived messages;
- open archived content in the local viewer;
- open the original chat;
- open or download standalone HTML when available.

The extension should remain useful without automatically parsing or importing entire conversations.

## Core principle

The user decides what is worth archiving.

The extension should not try to understand the entire provider interface or automatically capture every message.

The primary capture workflow is:

1. The user copies Markdown from the provider's own "Copy Markdown" action.
2. The user opens the extension's save action.
3. The extension attempts to obtain the copied Markdown from the clipboard.
4. The Markdown is shown in an editor.
5. The user can correct or clean up the Markdown.
6. A preview shows the rendered result.
7. The user explicitly saves the message.

If clipboard access is unavailable, the user should be able to paste the Markdown manually.

## Architecture

```text
AI chat page
     │
     ▼
Content Script
     │
     ├── Provider Adapter
     │      ├── provider
     │      ├── chat ID
     │      └── chat title
     │
     ├── Extension Application
     │
     ├── UI / Shadow DOM
     │
     └── API Client
              │
              ▼
       AI Chat Archive API
              │
              ▼
          FileStorage
              │
              ▼
       Markdown + JSON files
````

The extension communicates with the local application through its HTTP API.

The filesystem remains the source of truth.

## Provider integration

Provider-specific logic must be isolated behind provider adapters.

The first provider is ChatGPT.

The initial ChatGPT adapter should provide only what is actually required:

* determine whether the current page is supported;
* extract the chat ID from the URL;
* determine the chat title;
* observe chat title changes.

The adapter should not parse the entire conversation.

The extension should not depend on provider-specific DOM structures for message extraction unless a real use case requires this later.

## UI isolation

Extension UI is rendered inside Shadow DOM.

The purpose is to isolate:

* extension styles from provider styles;
* provider styles from extension styles;
* extension DOM from provider DOM.

The provider adapter and application logic must not depend on Shadow DOM internals.

Shadow DOM is a presentation boundary, not an application boundary.

## Editor

The editor is the main message-capture component.

It should provide:

* Markdown source editing;
* rendered preview;
* explicit Save action;
* Cancel action.

Markdown is the source of truth.

Preview is a derived representation.

The editor should not silently modify the source Markdown.

## Projects

Projects are the top-level organizational unit.

A project may contain chats from multiple providers.

Project management should eventually support:

* create;
* read;
* update;
* delete;
* project description;
* configurable storage location.

A default storage location may be provided by the application.

A project may override the default storage location.

Integration with IDE projects may be considered in the future but is not part of the initial implementation.

## Chats

Chats are primarily a read-oriented concept in the extension.

A chat is created automatically when the first message is saved.

The extension should eventually allow the user to:

* view chats belonging to a project;
* open the original provider chat;
* open the chat in the local viewer;
* open standalone HTML;
* download standalone HTML.

Chat editing and deletion are intentionally not part of the initial extension scope.

## Search

Search is primarily intended for finding information in a large archive.

The extension may provide a compact preview of search results.

Full reading should normally happen in the local viewer.

The existing API search model provides project, chat, message, and provider context.

Search should not become a second full-featured viewer inside the extension.

## Local API

The extension uses the existing HTTP API.

Current relevant operations include:

* list projects;
* get project;
* create project;
* list chats;
* get chat;
* create chat;
* create message;
* update message;
* search messages.

The API should be extended only when a real extension use case requires it.

The extension must not bypass the API and access the archive filesystem directly.

## Technology

Initial direction:

* TypeScript;
* HTML templates;
* SCSS;
* Shadow DOM;
* browser Content Scripts;
* a small build pipeline;
* no frontend framework initially.

A background service worker should only be introduced when a concrete browser API or use case requires it.

Do not introduce framework or build infrastructure solely for architectural completeness.

## Testing

Development follows a TDD workflow.

For each small behavior:

1. define one behavior;
2. write the test;
3. implement the smallest solution;
4. run the focused test;
5. fix failures;
6. run the complete extension test suite;
7. continue only when the suite is green.

The Python project follows the same principle.

Tests should keep application logic independent from provider DOM details wherever possible.

## Initial implementation plan

### Phase 1 — Extension foundation

* [ ] Create isolated extension project.
* [ ] Configure TypeScript.
* [ ] Configure build.
* [ ] Configure test runner.
* [ ] Create minimal browser extension manifest.
* [ ] Load a Content Script on ChatGPT.
* [ ] Create an isolated Shadow DOM root.
* [ ] Render a minimal Save button.

### Phase 2 — Save editor

* [ ] Open editor from Save button.
* [ ] Create Markdown source editor.
* [ ] Create Markdown preview.
* [ ] Add clipboard capture.
* [ ] Add manual paste fallback.
* [ ] Add Save / Cancel actions.

### Phase 3 — Chat context

* [ ] Detect ChatGPT provider.
* [ ] Extract chat ID from URL.
* [ ] Detect chat title.
* [ ] Observe title changes.
* [ ] Pass project/chat context to the save workflow.

### Phase 4 — API integration

* [ ] Connect extension API client to local API.
* [ ] Automatically create a chat when saving the first message.
* [ ] Save selected messages.
* [ ] Edit messages before saving.
* [ ] Handle API errors in the UI.

### Phase 5 — Projects

* [ ] Project list.
* [ ] Create project.
* [ ] Edit project.
* [ ] Delete project.
* [ ] Configure project storage location.
* [ ] Select active project.

### Phase 6 — Chats

* [ ] Project chat list.
* [ ] Chat preview.
* [ ] Open original provider chat.
* [ ] Open local viewer.
* [ ] Open standalone HTML.
* [ ] Download standalone HTML.

### Phase 7 — Search

* [ ] Search input.
* [ ] Search result preview.
* [ ] Project/chat/provider context.
* [ ] Open result in viewer.
* [ ] Navigate to the relevant message when a stable addressing mechanism is available.

### Future / intentionally deferred

* [ ] Additional AI providers.
* [ ] Automatic conversation import.
* [ ] Full conversation DOM parsing.
* [ ] IDE integration.
* [ ] Background service worker.
* [ ] Advanced synchronization.
* [ ] Search indexing.
* [ ] Database-backed storage.
* [ ] Automatic archival of all messages.

These features should only be implemented when a concrete use case requires them.

