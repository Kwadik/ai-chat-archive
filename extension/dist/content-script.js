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
  var create_project_default = '<form data-ai-chat-archive-create-project>\r\n    <p\r\n            data-ai-chat-archive-project-message\r\n            role="status"\r\n            hidden\r\n    ></p>\r\n    <label>\r\n        \u041D\u0430\u0437\u0432\u0430\u043D\u0438\u0435 \u043F\u0440\u043E\u0435\u043A\u0442\u0430\r\n        <input\r\n                type="text"\r\n                data-ai-chat-archive-project-name\r\n                required\r\n        />\r\n    </label>\r\n\r\n    <button\r\n            type="button"\r\n            data-ai-chat-archive-project-back\r\n    >\u041D\u0430\u0437\u0430\u0434</button>\r\n\r\n    <button type="submit">\u0421\u043E\u0437\u0434\u0430\u0442\u044C \u043F\u0440\u043E\u0435\u043A\u0442</button>\r\n</form>';

  // html-template:E:\PhpstormProjects\ai-chat-offline-viewer\extension\src\ui\templates\extension-panel.html
  var extension_panel_default = '<div data-ai-chat-archive-panel>\r\n    <div data-ai-chat-archive-header>\r\n        <span data-ai-chat-archive-title>AI Chat Archive</span>\r\n        <button\r\n                type="button"\r\n                data-ai-chat-archive-close\r\n                aria-label="\u0417\u0430\u043A\u0440\u044B\u0442\u044C \u043F\u0430\u043D\u0435\u043B\u044C"\r\n        >\xD7</button>\r\n    </div>\r\n\r\n    <div data-ai-chat-archive-content></div>\r\n</div>\r\n\r\n<button\r\n        type="button"\r\n        data-ai-chat-archive-open\r\n        aria-label="\u041E\u0442\u043A\u0440\u044B\u0442\u044C AI Chat Archive"\r\n        hidden\r\n>AI Chat Archive</button>';

  // html-template:E:\PhpstormProjects\ai-chat-offline-viewer\extension\src\ui\templates\screens\home.html
  var home_default = '<section data-ai-chat-archive-home>\r\n    <section data-ai-chat-archive-current-project>\r\n        <h2>\u0422\u0435\u043A\u0443\u0449\u0438\u0439 \u043F\u0440\u043E\u0435\u043A\u0442</h2>\r\n\r\n        <p data-ai-chat-archive-current-project-name>\r\n            \u041F\u0440\u043E\u0435\u043A\u0442 \u043D\u0435 \u0432\u044B\u0431\u0440\u0430\u043D\r\n        </p>\r\n\r\n        <div class="aca-actions">\r\n            <button\r\n                    type="button"\r\n                    data-ai-chat-archive-edit-project\r\n            >\u0420\u0435\u0434\u0430\u043A\u0442\u0438\u0440\u043E\u0432\u0430\u0442\u044C</button>\r\n\r\n            <button\r\n                    type="button"\r\n                    data-ai-chat-archive-show-projects\r\n            >\u0412\u0441\u0435 \u043F\u0440\u043E\u0435\u043A\u0442\u044B</button>\r\n\r\n            <button\r\n                    type="button"\r\n                    data-ai-chat-archive-create-project\r\n            >\u0421\u043E\u0437\u0434\u0430\u0442\u044C \u043F\u0440\u043E\u0435\u043A\u0442</button>\r\n        </div>\r\n    </section>\r\n\r\n    <section data-ai-chat-archive-current-chat>\r\n        <h2>\u0422\u0435\u043A\u0443\u0449\u0438\u0439 \u0447\u0430\u0442</h2>\r\n\r\n        <div class="aca-actions">\r\n            <button\r\n                    type="button"\r\n                    data-ai-chat-archive-save-chatgpt-message\r\n            >\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435 ChatGPT</button>\r\n\r\n            <button\r\n                    type="button"\r\n                    data-ai-chat-archive-save-user-message\r\n            >\u0421\u043E\u0445\u0440\u0430\u043D\u0438\u0442\u044C \u0441\u0432\u043E\u0451 \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u0435</button>\r\n        </div>\r\n    </section>\r\n</section>';

  // scss-template:E:\PhpstormProjects\ai-chat-offline-viewer\extension\src\ui\styles\extension-panel.scss
  var extension_panel_default2 = ":host {\n  --aca-color-primary: #2563eb;\n  --aca-color-primary-hover: #1d4ed8;\n  --aca-color-text: #222222;\n  --aca-color-muted: #6b7280;\n  --aca-color-surface: #ffffff;\n  --aca-color-surface-hover: #f5f7fb;\n  --aca-color-border: #e5e7eb;\n  --aca-font-family: Arial, sans-serif;\n  --aca-font-size: 14px;\n  --aca-font-size-small: 12px;\n  --aca-font-size-title: 16px;\n  --aca-space-1: 4px;\n  --aca-space-2: 8px;\n  --aca-space-3: 12px;\n  --aca-space-4: 16px;\n  --aca-radius-control: 8px;\n  --aca-radius-panel: 12px;\n}\n\n.aca-actions {\n  display: flex;\n  flex-wrap: wrap;\n  gap: var(--aca-space-2);\n}\n\n.aca-actions button {\n  box-sizing: border-box;\n  padding: var(--aca-space-2) var(--aca-space-3);\n  border: 1px solid var(--aca-color-border);\n  border-radius: var(--aca-radius-control);\n  background: var(--aca-color-surface);\n  color: var(--aca-color-text);\n  font: inherit;\n  cursor: pointer;\n  transition: background-color 120ms ease, border-color 120ms ease;\n}\n\n.aca-actions button:hover:not(:disabled) {\n  background: var(--aca-color-surface-hover);\n}\n\n.aca-actions button:focus-visible {\n  outline: 2px solid var(--aca-color-primary);\n  outline-offset: 2px;\n}\n\n.aca-actions button:disabled {\n  opacity: 0.5;\n  cursor: not-allowed;\n}\n\n[data-ai-chat-archive-open] {\n  pointer-events: auto;\n  position: absolute;\n  right: 16px;\n  bottom: 16px;\n  padding: 10px 16px;\n  border: 1px solid var(--aca-color-border);\n  border-radius: 999px;\n  background: var(--aca-color-surface);\n  color: var(--aca-color-text);\n  font: inherit;\n  cursor: pointer;\n}\n\n[data-ai-chat-archive-home] {\n  display: flex;\n  flex-direction: column;\n  gap: var(--aca-space-4);\n}\n\n[data-ai-chat-archive-current-project],\n[data-ai-chat-archive-current-chat] {\n  display: flex;\n  flex-direction: column;\n  gap: var(--aca-space-2);\n}\n\n[data-ai-chat-archive-home] h2 {\n  margin: 0;\n  font-size: var(--aca-font-size-title);\n  font-weight: 600;\n}\n\n[data-ai-chat-archive-home] p {\n  margin: 0;\n  color: var(--aca-color-muted);\n}\n\n[data-ai-chat-archive-home] h2 {\n  color: var(--aca-color-text);\n  line-height: 1.4;\n}\n\n[data-ai-chat-archive-panel] {\n  box-sizing: border-box;\n  font-family: var(--aca-font-family);\n  font-size: var(--aca-font-size);\n  color: var(--aca-color-text);\n  pointer-events: auto;\n  position: absolute;\n  top: 16px;\n  right: 16px;\n  width: min(480px, 100vw - 32px);\n  max-height: calc(100vh - 32px);\n  overflow-y: auto;\n  background: var(--aca-color-surface);\n  border: 1px solid var(--aca-color-border);\n  border-radius: var(--aca-radius-panel);\n  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);\n}\n\n[data-ai-chat-archive-header] {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  gap: var(--aca-space-4);\n  padding: var(--aca-space-3) var(--aca-space-4);\n  border-bottom: 1px solid var(--aca-color-border);\n}\n\n[data-ai-chat-archive-title] {\n  font-size: var(--aca-font-size-title);\n  font-weight: 600;\n}\n\n[data-ai-chat-archive-close] {\n  border: 0;\n  background: transparent;\n  color: var(--aca-color-muted);\n  font-size: 24px;\n  line-height: 1;\n  cursor: pointer;\n}\n\n[data-ai-chat-archive-content] {\n  padding: var(--aca-space-4);\n}\n\n[data-ai-chat-archive-close]:hover {\n  background: var(--aca-color-surface-hover);\n}\n\n[data-ai-chat-archive-close]:focus-visible {\n  outline: 2px solid var(--aca-color-primary);\n  outline-offset: 2px;\n}";

  // src/ui/extension-panel-styles.ts
  function getExtensionPanelStyles() {
    return extension_panel_default2;
  }

  // src/ui/extension-panel.ts
  function createExtensionPanel(root) {
    const existingPanel = root.shadowRoot?.querySelector(
      "[data-ai-chat-archive-panel]"
    );
    if (existingPanel instanceof HTMLDivElement) {
      return existingPanel;
    }
    const template = root.ownerDocument.createElement("template");
    template.innerHTML = extension_panel_default.trim();
    const fragment = template.content.cloneNode(true);
    const panel = fragment.querySelector(
      "[data-ai-chat-archive-panel]"
    );
    const openButton = fragment.querySelector(
      "[data-ai-chat-archive-open]"
    );
    const closeButton = panel.querySelector(
      "[data-ai-chat-archive-close]"
    );
    closeButton.addEventListener("click", () => {
      panel.hidden = true;
      openButton.hidden = false;
    });
    openButton.addEventListener("click", () => {
      panel.hidden = false;
      openButton.hidden = true;
    });
    const styles = createStylesheet(
      root.ownerDocument,
      getExtensionPanelStyles()
    );
    root.shadowRoot?.prepend(styles);
    root.shadowRoot?.appendChild(fragment);
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
  function showProjectCreation(panel, initialName = "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442", onSubmit, onBack, context) {
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
      context?.data?.projectName ?? initialName
    );
    const message = form.querySelector(
      "[data-ai-chat-archive-project-message]"
    );
    if (message instanceof HTMLParagraphElement && context?.message) {
      message.textContent = context.message;
      message.hidden = false;
    }
    const backButton = form.querySelector(
      "[data-ai-chat-archive-project-back]"
    );
    if (backButton instanceof HTMLButtonElement && onBack) {
      backButton.addEventListener("click", onBack);
    }
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
  function showHomeScreen(panel, options) {
    const content = panel.querySelector(
      "[data-ai-chat-archive-content]"
    );
    if (!(content instanceof HTMLDivElement)) {
      throw new Error("Extension panel content not found");
    }
    const template = panel.ownerDocument.createElement("template");
    template.innerHTML = home_default.trim();
    const screen = template.content.firstElementChild;
    if (!(screen instanceof HTMLElement)) {
      throw new Error("Home screen template is empty");
    }
    const projectName = screen.querySelector(
      "[data-ai-chat-archive-current-project-name]"
    );
    if (projectName) {
      projectName.textContent = options.currentProjectName ?? "\u041F\u0440\u043E\u0435\u043A\u0442 \u043D\u0435 \u0432\u044B\u0431\u0440\u0430\u043D";
    }
    const bindClick = (selector, callback) => {
      const button = screen.querySelector(selector);
      if (!(button instanceof HTMLButtonElement)) {
        throw new Error(`Home screen button not found: ${selector}`);
      }
      button.addEventListener("click", callback);
    };
    bindClick(
      "[data-ai-chat-archive-show-projects]",
      options.onShowProjects
    );
    bindClick(
      "[data-ai-chat-archive-create-project]",
      options.onCreateProject
    );
    bindClick(
      "[data-ai-chat-archive-edit-project]",
      options.onEditProject
    );
    bindClick(
      "[data-ai-chat-archive-save-chatgpt-message]",
      options.onSaveChatGPTMessage
    );
    bindClick(
      "[data-ai-chat-archive-save-user-message]",
      options.onSaveUserMessage
    );
    content.replaceChildren(screen);
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
    const showProjects = async (initialMarkdown, onSelect) => {
      const projects = await options.listProjects();
      showProjectSelection(
        panel,
        projects,
        async (projectId) => {
          await options.saveSelectedProjectId?.(projectId);
          options.selectedProjectId = projectId;
          if (onSelect) {
            await onSelect(projectId);
            return;
          }
          showExtensionEditor(
            panel,
            initialMarkdown,
            (markdown) => onSave(markdown, context),
            onCancel
          );
        },
        () => {
          showProjectCreation(
            panel,
            "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442",
            async (name) => {
              const project = await options.createProject(name);
              await options.saveSelectedProjectId?.(project.id);
              options.selectedProjectId = project.id;
              if (onSelect) {
                await onSelect(project.id);
                return;
              }
              showExtensionEditor(
                panel,
                initialMarkdown,
                (markdown) => onSave(markdown, context),
                onCancel
              );
            },
            () => {
              void showProjects(initialMarkdown, onSelect);
            },
            {
              returnTo: "project-selection",
              data: {
                projectName: "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442"
              }
            }
          );
        }
      );
    };
    return {
      context,
      async openHome() {
        const projects = await options.listProjects();
        const selectedProject = projects.find(
          (project) => project.id === options.selectedProjectId
        );
        showHomeScreen(panel, {
          currentProjectName: selectedProject?.name ?? null,
          onShowProjects: () => {
            void showProjects("", () => this.openHome());
          },
          onCreateProject: () => {
            showProjectCreation(
              panel,
              "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442",
              async (name) => {
                const project = await options.createProject(name);
                await options.saveSelectedProjectId?.(project.id);
                options.selectedProjectId = project.id;
                await this.openHome();
              },
              () => {
                void this.openHome();
              },
              {
                returnTo: "home",
                data: {
                  projectName: "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442"
                }
              }
            );
          },
          onEditProject: () => {
          },
          onSaveChatGPTMessage: () => {
          },
          onSaveUserMessage: () => {
          }
        });
      },
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
                showProjectCreation(
                  panel,
                  "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442",
                  async (name) => {
                    const project = await options.createProject(name);
                    await options.saveSelectedProjectId?.(project.id);
                    options.selectedProjectId = project.id;
                    this.openEditor(markdown ?? "");
                  },
                  () => {
                    void options.listProjects().then((projects2) => {
                      showProjectSelection(
                        panel,
                        projects2,
                        async (projectId) => {
                          await options.saveSelectedProjectId?.(projectId);
                          options.selectedProjectId = projectId;
                          this.openEditor(markdown ?? "");
                        },
                        () => {
                        }
                      );
                    });
                  },
                  {
                    returnTo: "project-selection",
                    data: {
                      projectName: "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442"
                    }
                  }
                );
              }
            );
            return;
          }
          showProjectCreation(
            panel,
            "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442",
            async (name) => {
              const project = await options.createProject(name);
              await options.saveSelectedProjectId?.(project.id);
              options.selectedProjectId = project.id;
              showExtensionEditor(
                panel,
                markdown ?? "",
                (markdown2) => onSave(markdown2, context),
                onCancel
              );
            },
            void 0,
            {
              returnTo: "home",
              message: "\u0414\u043B\u044F \u0441\u043E\u0445\u0440\u0430\u043D\u0435\u043D\u0438\u044F \u0441\u043E\u043E\u0431\u0449\u0435\u043D\u0438\u044F \u043D\u0435\u043E\u0431\u0445\u043E\u0434\u0438\u043C\u043E \u0432\u044B\u0431\u0440\u0430\u0442\u044C \u0438\u043B\u0438 \u0441\u043E\u0437\u0434\u0430\u0442\u044C \u043F\u0440\u043E\u0435\u043A\u0442.",
              data: {
                projectName: "\u041C\u043E\u0439 \u043F\u0440\u043E\u0435\u043A\u0442"
              }
            }
          );
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
