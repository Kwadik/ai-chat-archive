"use strict";
(() => {
  // src/providers/chatgpt-url.ts
  function getChatIdFromChatGPTUrl(url) {
    const match = url.pathname.match(/^\/c\/([^/]+)$/);
    return match ? match[1] : null;
  }

  // src/providers/chatgpt.ts
  var chatgptProvider = {
    provider: "chatgpt",
    canHandle(url) {
      return url.hostname === "chatgpt.com";
    },
    getChatId(url) {
      return getChatIdFromChatGPTUrl(url);
    },
    getChatUrl(chatId) {
      return `https://chatgpt.com/c/${chatId}`;
    },
    getChatTitle(document2) {
      const title = document2.title.trim();
      return title || null;
    }
  };

  // src/content.ts
  function getCurrentProvider(url) {
    if (chatgptProvider.canHandle(url)) {
      return chatgptProvider;
    }
    return null;
  }
  function getCurrentChatContext(url, document2) {
    const provider = getCurrentProvider(url);
    if (!provider) {
      return null;
    }
    const chatId = provider.getChatId(url);
    if (!chatId) {
      return null;
    }
    return {
      provider: provider.provider,
      chatId,
      title: provider.getChatTitle(document2)
    };
  }

  // src/clipboard.ts
  async function readMarkdownFromClipboard(clipboard) {
    if (clipboard === null) {
      return null;
    }
    try {
      return await clipboard.readText();
    } catch {
      return null;
    }
  }

  // src/extension-root.ts
  function createExtensionRoot(document2) {
    const existingRoot = document2.getElementById(
      "ai-chat-archive-root"
    );
    if (existingRoot instanceof HTMLDivElement) {
      return existingRoot;
    }
    const root = document2.createElement("div");
    root.id = "ai-chat-archive-root";
    root.style.position = "fixed";
    root.style.inset = "0";
    root.style.pointerEvents = "none";
    root.attachShadow({ mode: "open" });
    document2.body.appendChild(root);
    return root;
  }

  // src/extension-editor.ts
  function createExtensionEditor(initialMarkdown, onSave, onCancel) {
    const editor = document.createElement("div");
    const textarea = document.createElement("textarea");
    textarea.dataset.aiChatArchiveEditor = "";
    textarea.value = initialMarkdown;
    const actions = document.createElement("div");
    const cancelButton = document.createElement("button");
    cancelButton.dataset.aiChatArchiveCancel = "";
    cancelButton.type = "button";
    cancelButton.textContent = "Cancel";
    cancelButton.addEventListener("click", () => {
      onCancel();
    });
    const saveButton = document.createElement("button");
    saveButton.dataset.aiChatArchiveSave = "";
    saveButton.type = "button";
    saveButton.textContent = "Save";
    saveButton.addEventListener("click", () => {
      onSave(textarea.value);
    });
    actions.appendChild(cancelButton);
    actions.appendChild(saveButton);
    editor.appendChild(textarea);
    editor.appendChild(actions);
    return editor;
  }

  // src/extension-panel.ts
  function createExtensionPanel(root) {
    const existingPanel = root.shadowRoot?.querySelector(
      "[data-ai-chat-archive-panel]"
    );
    if (existingPanel instanceof HTMLDivElement) {
      return existingPanel;
    }
    const panel = document.createElement("div");
    panel.dataset.aiChatArchivePanel = "";
    panel.style.pointerEvents = "auto";
    panel.style.position = "absolute";
    panel.style.top = "16px";
    panel.style.right = "16px";
    panel.style.minWidth = "320px";
    panel.style.maxWidth = "480px";
    panel.style.maxHeight = "calc(100vh - 32px)";
    panel.style.overflowY = "auto";
    panel.style.background = "white";
    const header = document.createElement("div");
    header.dataset.aiChatArchiveHeader = "";
    const title = document.createElement("span");
    title.dataset.aiChatArchiveTitle = "";
    title.textContent = "AI Chat Archive";
    const closeButton = document.createElement("button");
    closeButton.dataset.aiChatArchiveClose = "";
    closeButton.type = "button";
    closeButton.textContent = "\xD7";
    closeButton.addEventListener("click", () => {
      panel.hidden = true;
    });
    header.appendChild(title);
    header.appendChild(closeButton);
    const content = document.createElement("div");
    content.dataset.aiChatArchiveContent = "";
    panel.appendChild(header);
    panel.appendChild(content);
    root.shadowRoot?.appendChild(panel);
    return panel;
  }
  function showExtensionEditor(panel, initialMarkdown, onSave, onCancel) {
    const content = panel.querySelector(
      "[data-ai-chat-archive-content]"
    );
    if (!(content instanceof HTMLDivElement)) {
      throw new Error("Extension panel content not found");
    }
    content.replaceChildren();
    const editor = createExtensionEditor(
      initialMarkdown,
      onSave,
      onCancel
    );
    content.appendChild(editor);
    panel.hidden = false;
  }

  // src/extension-ui.ts
  function createExtensionUI(document2, context, onSave, onCancel, clipboard) {
    const root = createExtensionRoot(document2);
    const panel = createExtensionPanel(root);
    return {
      context,
      openEditor(initialMarkdown) {
        showExtensionEditor(
          panel,
          initialMarkdown,
          (markdown) => {
            onSave(markdown, context);
          },
          onCancel
        );
      },
      async openEditorFromClipboard() {
        const markdown = await readMarkdownFromClipboard(
          clipboard
        );
        this.openEditor(markdown ?? "");
      }
    };
  }

  // src/content-ui.ts
  function createContentUI(document2, context, onSave, onCancel, clipboard) {
    return createExtensionUI(
      document2,
      context,
      onSave,
      onCancel,
      clipboard
    );
  }

  // src/content-ui-runtime.ts
  function initializeContentUI(document2, url, onSave, onCancel, clipboard) {
    const context = getCurrentChatContext(
      url,
      {
        title: document2.title
      }
    );
    if (!context) {
      return null;
    }
    return createContentUI(
      document2,
      context,
      onSave,
      onCancel,
      clipboard
    );
  }

  // src/content-runtime.ts
  function runContentScript(runtime, document2, onSave, onCancel, clipboard) {
    return initializeContentUI(
      document2,
      new URL(runtime.location.href),
      onSave,
      onCancel,
      clipboard
    );
  }

  // src/browser-content-runtime.ts
  function runBrowserContentScript() {
    return runContentScript(
      {
        location: {
          href: window.location.href
        }
      },
      document,
      () => {
      },
      () => {
      },
      navigator.clipboard ?? null
    );
  }

  // src/content-script.ts
  runBrowserContentScript();
})();
