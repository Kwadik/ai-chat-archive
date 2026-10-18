import { createExtensionEditor } from "./extension-editor";
import { createProjectForm } from "./create-project-template";
import { createStylesheet } from "./create-stylesheet";
import createProjectTemplate from "./templates/create-project.html?raw";
import extensionPanelTemplate from "./templates/extension-panel.html?raw";
import homeTemplate from "./templates/screens/home.html?raw";
import { getExtensionPanelStyles } from "./extension-panel-styles";
import type { ProjectCreationContext } from "./navigation-context";

export function createExtensionPanel(
    root: HTMLDivElement,
): HTMLDivElement {
    const existingPanel = root.shadowRoot?.querySelector(
        '[data-ai-chat-archive-panel]',
    );

    if (existingPanel instanceof HTMLDivElement) {
        return existingPanel;
    }

    const template = root.ownerDocument.createElement("template");
    template.innerHTML = extensionPanelTemplate.trim();

    const fragment = template.content.cloneNode(true) as DocumentFragment;

    const panel = fragment.querySelector(
        "[data-ai-chat-archive-panel]",
    ) as HTMLDivElement;

    const openButton = fragment.querySelector(
        "[data-ai-chat-archive-open]",
    ) as HTMLButtonElement;

    const closeButton = panel.querySelector(
        "[data-ai-chat-archive-close]",
    ) as HTMLButtonElement;

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
        getExtensionPanelStyles(),
    );

    root.shadowRoot?.prepend(styles);
    root.shadowRoot?.appendChild(fragment);

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
    onBack?: () => void,
    context?: ProjectCreationContext,
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
        context?.data?.projectName ?? initialName,
    );

    const message = form.querySelector(
        "[data-ai-chat-archive-project-message]",
    );

    if (message instanceof HTMLParagraphElement && context?.message) {
        message.textContent = context.message;
        message.hidden = false;
    }

    const backButton = form.querySelector(
        "[data-ai-chat-archive-project-back]",
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

export interface HomeScreenOptions {
    currentProjectName: string | null;
    onShowProjects: () => void;
    onCreateProject: () => void;
    onEditProject: () => void;
    onSaveChatGPTMessage: () => void;
    onSaveUserMessage: () => void;
}

export function showHomeScreen(
    panel: HTMLDivElement,
    options: HomeScreenOptions,
): void {
    const content = panel.querySelector(
        "[data-ai-chat-archive-content]",
    );

    if (!(content instanceof HTMLDivElement)) {
        throw new Error("Extension panel content not found");
    }

    const template = panel.ownerDocument.createElement("template");
    template.innerHTML = homeTemplate.trim();

    const screen = template.content.firstElementChild;

    if (!(screen instanceof HTMLElement)) {
        throw new Error("Home screen template is empty");
    }

    const projectName = screen.querySelector(
        "[data-ai-chat-archive-current-project-name]",
    );

    if (projectName) {
        projectName.textContent =
            options.currentProjectName ?? "Проект не выбран";
    }

    const bindClick = (
        selector: string,
        callback: () => void,
    ): void => {
        const button = screen.querySelector(selector);

        if (!(button instanceof HTMLButtonElement)) {
            throw new Error(`Home screen button not found: ${selector}`);
        }

        button.addEventListener("click", callback);
    };

    bindClick(
        "[data-ai-chat-archive-show-projects]",
        options.onShowProjects,
    );
    bindClick(
        "[data-ai-chat-archive-create-project]",
        options.onCreateProject,
    );
    bindClick(
        "[data-ai-chat-archive-edit-project]",
        options.onEditProject,
    );
    bindClick(
        "[data-ai-chat-archive-save-chatgpt-message]",
        options.onSaveChatGPTMessage,
    );
    bindClick(
        "[data-ai-chat-archive-save-user-message]",
        options.onSaveUserMessage,
    );

    content.replaceChildren(screen);
    panel.hidden = false;
}