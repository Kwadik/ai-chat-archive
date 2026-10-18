import { createExtensionEditor } from "./extension-editor";
import { createProjectForm } from "./create-project-template";
import { createStylesheet } from "./create-stylesheet";
import createProjectTemplate from "./templates/create-project.html?raw";
import { getExtensionPanelStyles } from "./extension-panel-styles";

export function createExtensionPanel(
    root: HTMLDivElement,
): HTMLDivElement {
    const existingPanel = root.shadowRoot?.querySelector(
        '[data-ai-chat-archive-panel]',
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
    closeButton.textContent = "×";

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
        getExtensionPanelStyles(),
    );

    root.shadowRoot?.prepend(styles);
    root.shadowRoot?.appendChild(panel);

    return panel;
}

export function showExtensionEditor(
    panel: HTMLDivElement,
    initialMarkdown: string,
    onSave: (markdown: string) => void,
    onCancel: () => void,
): void {
    const content = panel.querySelector(
        "[data-ai-chat-archive-content]",
    );

    if (!(content instanceof HTMLDivElement)) {
        throw new Error("Extension panel content not found");
    }

    content.replaceChildren();

    const editor = createExtensionEditor(
        initialMarkdown,
        onSave,
        onCancel,
    );

    content.appendChild(editor);

    panel.hidden = false;
}

export function showProjectCreation(
    panel: HTMLDivElement,
    initialName = "Мой проект",
    onSubmit?: (name: string) => void | Promise<void>,
): void {
    const content = panel.querySelector(
        "[data-ai-chat-archive-content]",
    );

    if (!(content instanceof HTMLDivElement)) {
        throw new Error("Extension panel content not found");
    }

    content.replaceChildren();

    const form = createProjectForm(
        panel.ownerDocument,
        createProjectTemplate,
        initialName,
    );

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (!onSubmit) {
            return;
        }

        const nameInput = form.querySelector(
            "[data-ai-chat-archive-project-name]",
        );

        if (!(nameInput instanceof HTMLInputElement)) {
            throw new Error("Project name input not found");
        }

        void onSubmit(nameInput.value.trim());
    });

    content.appendChild(form);
    panel.hidden = false;
}

export function showProjectSelection(
    panel: HTMLDivElement,
    projects: { id: string; name: string }[],
    onSelect: (projectId: string) => void,
    onCreateProject: () => void,
): void {
    const content = panel.querySelector(
        "[data-ai-chat-archive-content]",
    );

    if (!(content instanceof HTMLDivElement)) {
        throw new Error("Extension panel content not found");
    }

    content.replaceChildren();

    const selector = panel.ownerDocument.createElement("div");
    selector.dataset.aiChatArchiveProjectSelector = "";

    const title = panel.ownerDocument.createElement("h2");
    title.textContent = "Выберите проект";
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
    createButton.textContent = "Создать новый проект";

    createButton.addEventListener("click", onCreateProject);

    selector.appendChild(createButton);
    content.appendChild(selector);

    panel.hidden = false;
}