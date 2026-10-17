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

    content.appendChild(form);

    panel.hidden = false;
}