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

  // src/chat/content.ts
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

  // src/clipboard/clipboard.ts
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

  // src/ui/extension-root.ts
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

  // src/ui/extension-editor.ts
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

  // src/ui/create-project-template.ts
  function createProjectForm(document2, templateHtml, initialName = "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442") {
    const template = document2.createElement("template");
    template.innerHTML = templateHtml.trim();
    const form = template.content.querySelector(
      "[data-ai-chat-archive-create-project]"
    );
    if (!(form instanceof HTMLFormElement)) {
      throw new Error("Project creation form template not found");
    }
    const nameInput = form.querySelector(
      "[data-ai-chat-archive-project-name]"
    );
    if (!(nameInput instanceof HTMLInputElement)) {
      throw new Error("Project name input not found");
    }
    nameInput.value = initialName;
    return form;
  }

  // src/ui/create-stylesheet.ts
  function createStylesheet(document2, cssText) {
    const styles = document2.createElement("style");
    styles.dataset.aiChatArchiveStyles = "";
    styles.textContent = cssText;
    return styles;
  }

  // html-template:E:\PhpstormProjects\ai-chat-offline-viewer\extension\src\ui\templates\create-project.html
  var create_project_default = '<form data-ai-chat-archive-create-project>\r\n    <label>\r\n        \u041D\u0430\u0437\u0432\u0430\u043D\u0438\u0435 \u043F\u0440\u043E\u0435\u043A\u0442\u0430\r\n        <input\r\n                type="text"\r\n                data-ai-chat-archive-project-name\r\n                required\r\n        />\r\n    </label>\r\n\r\n    <button type="submit">\u0421\u043E\u0437\u0434\u0430\u0442\u044C \u043F\u0440\u043E\u0435\u043A\u0442</button>\r\n</form>';

  // scss-template:E:\PhpstormProjects\ai-chat-offline-viewer\extension\src\ui\styles\extension-panel.scss
  var extension_panel_default = "[data-ai-chat-archive-panel] {\n  box-sizing: border-box;\n  font-family: Arial, sans-serif;\n  color: #222;\n  pointer-events: auto;\n  position: absolute;\n  top: 16px;\n  right: 16px;\n  min-width: 320px;\n  max-width: 480px;\n  max-height: calc(100vh - 32px);\n  overflow-y: auto;\n  background: white;\n}";

  // src/ui/extension-panel-styles.ts
  function getExtensionPanelStyles() {
    return extension_panel_default;
  }

  // src/ui/extension-panel.ts
  function createExtensionPanel(root) {
    const existingPanel = root.shadowRoot?.querySelector(
      "[data-ai-chat-archive-panel]"
    );
    if (existingPanel instanceof HTMLDivElement) {
      return existingPanel;
    }
    const panel = document.createElement("div");
    panel.dataset.aiChatArchivePanel = "";
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
    const styles = createStylesheet(
      panel.ownerDocument,
      getExtensionPanelStyles()
    );
    root.shadowRoot?.prepend(styles);
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
  function showProjectCreation(panel, initialName = "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442", onSubmit) {
    const content = panel.querySelector(
      "[data-ai-chat-archive-content]"
    );
    if (!(content instanceof HTMLDivElement)) {
      throw new Error("Extension panel content not found");
    }
    content.replaceChildren();
    const form = createProjectForm(
      panel.ownerDocument,
      create_project_default,
      initialName
    );
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!onSubmit) {
        return;
      }
      const nameInput = form.querySelector(
        "[data-ai-chat-archive-project-name]"
      );
      if (!(nameInput instanceof HTMLInputElement)) {
        throw new Error("Project name input not found");
      }
      void onSubmit(nameInput.value.trim());
    });
    content.appendChild(form);
    panel.hidden = false;
  }
  function showProjectSelection(panel, projects, onSelect, onCreateProject) {
    const content = panel.querySelector(
      "[data-ai-chat-archive-content]"
    );
    if (!(content instanceof HTMLDivElement)) {
      throw new Error("Extension panel content not found");
    }
    content.replaceChildren();
    const selector = panel.ownerDocument.createElement("div");
    selector.dataset.aiChatArchiveProjectSelector = "";
    const title = panel.ownerDocument.createElement("h2");
    title.textContent = "\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u043F\u0440\u043E\u0435\u043A\u0442";
    selector.appendChild(title);
    for (const project of projects) {
      const button = panel.ownerDocument.createElement("button");
      button.type = "button";
      button.textContent = project.name;
      button.addEventListener("click", () => {
        onSelect(project.id);
      });
      selector.appendChild(button);
    }
    const createButton = panel.ownerDocument.createElement("button");
    createButton.type = "button";
    createButton.dataset.aiChatArchiveCreateProject = "";
    createButton.textContent = "\u0421\u043E\u0437\u0434\u0430\u0442\u044C \u043D\u043E\u0432\u044B\u0439 \u043F\u0440\u043E\u0435\u043A\u0442";
    createButton.addEventListener("click", onCreateProject);
    selector.appendChild(createButton);
    content.appendChild(selector);
    panel.hidden = false;
  }

  // src/ui/extension-ui.ts
  function createExtensionUI(document2, context, onSave, onCancel, clipboard, options = {
    selectedProjectId: "existing-project",
    createProject: async () => {
      throw new Error("Project creation is not configured");
    },
    listProjects: async () => []
  }) {
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
        const markdown = await readMarkdownFromClipboard(clipboard);
        const projects = options.selectedProjectId === null ? await options.listProjects() : [];
        if (options.selectedProjectId === null) {
          if (projects.length > 0) {
            showProjectSelection(
              panel,
              projects,
              async (projectId) => {
                await options.saveSelectedProjectId?.(projectId);
                options.selectedProjectId = projectId;
                this.openEditor(markdown ?? "");
              },
              () => {
                showProjectCreation(panel, "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442", async (name) => {
                  const project = await options.createProject(name);
                  await options.saveSelectedProjectId?.(project.id);
                  options.selectedProjectId = project.id;
                  showExtensionEditor(
                    panel,
                    markdown ?? "",
                    (markdown2) => onSave(markdown2, context),
                    onCancel
                  );
                });
              }
            );
            return;
          }
          showProjectCreation(panel, "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442", async (name) => {
            const project = await options.createProject(name);
            await options.saveSelectedProjectId?.(project.id);
            options.selectedProjectId = project.id;
            showExtensionEditor(
              panel,
              markdown ?? "",
              (markdown2) => onSave(markdown2, context),
              onCancel
            );
          });
          return;
        }
        this.openEditor(markdown ?? "");
      }
    };
  }

  // src/chat/content-ui.ts
  function createContentUI(document2, context, onSave, onCancel, clipboard, options) {
    return createExtensionUI(
      document2,
      context,
      onSave,
      onCancel,
      clipboard,
      options
    );
  }

  // src/chat/content-ui-runtime.ts
  function initializeContentUI(document2, url, onSave, onCancel, clipboard, options) {
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
      clipboard,
      options
    );
  }

  // src/chat/content-runtime.ts
  function runContentScript(runtime, document2, onSave, onCancel, clipboard, options) {
    return initializeContentUI(
      document2,
      new URL(runtime.location.href),
      onSave,
      onCancel,
      clipboard,
      options
    );
  }

  // src/save/save-message.ts
  async function saveMessage(apiClient, context, markdown, projectId) {
    return apiClient.createMessage({
      projectId,
      provider: context.provider,
      chatId: context.chatId,
      role: "user",
      content: markdown
    });
  }

  // src/chat/browser-content-runtime.ts
  function runBrowserContentScript(onSave = () => {
  }, onCancel = () => {
  }, apiClient, projectId = null, uiOptions) {
    return runContentScript(
      {
        location: {
          href: window.location.href
        }
      },
      document,
      (markdown, context) => {
        const selectedProjectId = uiOptions?.selectedProjectId ?? projectId;
        if (apiClient && selectedProjectId !== null) {
          void saveMessage(
            apiClient,
            context,
            markdown,
            selectedProjectId
          );
        }
        onSave(markdown, context);
      },
      onCancel,
      navigator.clipboard ?? null,
      uiOptions
    );
  }

  // src/api/api-client.ts
  var ExtensionApiClient = class {
    constructor(baseUrl, fetchFn = fetch) {
      this.baseUrl = baseUrl;
      this.fetchFn = fetchFn;
    }
    baseUrl;
    fetchFn;
    async createMessage(input) {
      const url = `${this.baseUrl}/projects/${input.projectId}/chats/${input.provider}/${input.chatId}/messages`;
      const response = await this.fetchFn(
        url,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            role: input.role,
            content: input.content
          })
        }
      );
      if (!response.ok) {
        throw new Error(
          `API request failed with status ${response.status}`
        );
      }
      return response.json();
    }
    async listProjects() {
      const response = await this.fetchFn(
        `${this.baseUrl}/projects`,
        {
          method: "GET"
        }
      );
      if (!response.ok) {
        throw new Error(
          `API request failed with status ${response.status}`
        );
      }
      return response.json();
    }
    async createProject(input) {
      const response = await this.fetchFn(
        `${this.baseUrl}/projects`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(input)
        }
      );
      if (!response.ok) {
        throw new Error(
          `API request failed with status ${response.status}`
        );
      }
      return response.json();
    }
  };

  // src/api/browser-api-client.ts
  var DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";
  function createBrowserApiClient(baseUrl = DEFAULT_API_BASE_URL) {
    return new ExtensionApiClient(baseUrl);
  }

  // src/storage/browser-storage.ts
  function getBrowserStorage(chrome2) {
    return chrome2.storage;
  }

  // src/storage/extension-storage.ts
  var SELECTED_PROJECT_KEY = "selectedProjectId";
  async function setStoredProjectId(projectId, storage) {
    await storage.local.set({
      [SELECTED_PROJECT_KEY]: projectId
    });
  }
  async function getStoredProjectId(storage) {
    const values = await storage.local.get(
      SELECTED_PROJECT_KEY
    );
    const projectId = values[SELECTED_PROJECT_KEY];
    return typeof projectId === "string" ? projectId : null;
  }

  // src/project/project-config.ts
  async function getSelectedProjectId(storage) {
    const projectId = await getStoredProjectId(storage);
    return projectId ?? null;
  }

  // src/chat/browser-content-script.ts
  async function initializeBrowserContentScript(chrome2, apiClient, run = runBrowserContentScript) {
    const storage = getBrowserStorage(chrome2);
    const projectId = await getSelectedProjectId(storage);
    const uiOptions = {
      selectedProjectId: projectId,
      listProjects: () => apiClient.listProjects(),
      createProject: (name) => apiClient.createProject({
        id: crypto.randomUUID(),
        name
      }),
      saveSelectedProjectId: (id) => setStoredProjectId(id, storage)
    };
    run(
      () => {
      },
      () => {
      },
      apiClient,
      projectId,
      uiOptions
    );
  }

  // src/content-script.ts
  void initializeBrowserContentScript(
    chrome,
    createBrowserApiClient(),
    runBrowserContentScript
  );
})();
