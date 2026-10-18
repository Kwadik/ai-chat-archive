/**
 * @vitest-environment jsdom
 */
import {
    describe,
    expect,
    it,
    vi,
} from "vitest";
import { createExtensionRoot } from "../../src/ui/extension-root";
import {
    createExtensionPanel,
    showExtensionEditor,
    showProjectSelection,
    showHomeScreen,
    showProjectCreation,
} from "../../src/ui/extension-panel";

describe("extension panel", () => {
    it("creates a panel with header and content area", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        expect(panel.querySelector("[data-ai-chat-archive-header]"))
            .not.toBeNull();

        expect(panel.querySelector("[data-ai-chat-archive-content]"))
            .not.toBeNull();
    });

    it("shows the application title", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        expect(
            panel.querySelector("[data-ai-chat-archive-title]")?.textContent,
        ).toBe("AI Chat Archive");
    });

    it("provides a close button", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        const closeButton = panel.querySelector(
            "[data-ai-chat-archive-close]",
        );

        expect(closeButton).not.toBeNull();
        expect(closeButton?.textContent).toBe("×");
    });

    it("shows the open button when the panel is closed", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        const closeButton = panel.querySelector(
            "[data-ai-chat-archive-close]",
        ) as HTMLButtonElement;

        const openButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-open]",
        ) as HTMLButtonElement;

        expect(panel.hidden).toBe(false);
        expect(openButton.hidden).toBe(true);

        closeButton.click();

        expect(panel.hidden).toBe(true);
        expect(openButton.hidden).toBe(false);
    });

    it("reopens the panel when the open button is clicked", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        const closeButton = panel.querySelector(
            "[data-ai-chat-archive-close]",
        ) as HTMLButtonElement;

        const openButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-open]",
        ) as HTMLButtonElement;

        closeButton.click();
        openButton.click();

        expect(panel.hidden).toBe(false);
        expect(openButton.hidden).toBe(true);
    });

    it("keeps the same panel instance", () => {
        const root = createExtensionRoot(document);

        const first = createExtensionPanel(root);
        const second = createExtensionPanel(root);

        expect(second).toBe(first);
    });

    it("shows the Markdown editor", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        showExtensionEditor(
            panel,
            "Hello **world**",
            vi.fn(),
            vi.fn(),
        );

        const textarea = panel.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        expect(textarea).not.toBeNull();
        expect(textarea.value).toBe("Hello **world**");
    });

    it("passes edited Markdown to the save callback", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);
        const onSave = vi.fn();

        showExtensionEditor(
            panel,
            "Initial",
            onSave,
            vi.fn(),
        );

        const textarea = panel.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        textarea.value = "Edited";

        const saveButton = panel.querySelector(
            "[data-ai-chat-archive-save]",
        ) as HTMLButtonElement;

        saveButton.click();

        expect(onSave).toHaveBeenCalledWith("Edited");
    });

    it("shows the panel when the editor is displayed", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        panel.hidden = true;

        showExtensionEditor(
            panel,
            "Markdown",
            vi.fn(),
            vi.fn(),
        );

        expect(panel.hidden).toBe(false);
    });

    it("adds a stylesheet inside Shadow DOM", () => {
        const root = createExtensionRoot(document);
        createExtensionPanel(root);

        const styles = root.shadowRoot?.querySelector(
            "style[data-ai-chat-archive-styles]",
        );

        expect(styles).not.toBeNull();
    });

    it("does not duplicate the stylesheet", () => {
        const root = createExtensionRoot(document);

        createExtensionPanel(root);
        createExtensionPanel(root);

        expect(
            root.shadowRoot?.querySelectorAll(
                "style[data-ai-chat-archive-styles]",
            ).length,
        ).toBe(1);
    });

    it("shows available projects for selection", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        showProjectSelection(panel, [
            { id: "project-1", name: "Рабочий проект" },
            { id: "project-2", name: "Личный проект" },
        ], vi.fn(), vi.fn());

        expect(
            panel.querySelector("[data-ai-chat-archive-project-selector]"),
        ).not.toBeNull();

        expect(panel.textContent).toContain("Рабочий проект");
        expect(panel.textContent).toContain("Личный проект");

        expect(
            panel.querySelector("[data-ai-chat-archive-create-project]"),
        ).not.toBeNull();

        expect(panel.hidden).toBe(false);
    });

    it("shows the home screen with project and message actions", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        showHomeScreen(panel, {
            currentProjectName: "Рабочий проект",
            onShowProjects: vi.fn(),
            onCreateProject: vi.fn(),
            onEditProject: vi.fn(),
            onSaveChatGPTMessage: vi.fn(),
            onSaveUserMessage: vi.fn(),
        });

        expect(panel.textContent).toContain("Рабочий проект");
        expect(panel.textContent).toContain("Все проекты");
        expect(panel.textContent).toContain("Создать проект");
        expect(panel.textContent).toContain("Сохранить сообщение ChatGPT");
        expect(panel.textContent).toContain("Сохранить своё сообщение");
    });

    it("uses project creation context for message and initial name", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        showProjectCreation(
            panel,
            "Мой проект",
            undefined,
            undefined,
            {
                returnTo: "home",
                message: "Для сохранения сообщения необходимо выбрать проект",
                data: {
                    projectName: "Рабочий проект",
                },
            },
        );

        const message = panel.querySelector(
            "[data-ai-chat-archive-project-message]",
        );
        const nameInput = panel.querySelector(
            "[data-ai-chat-archive-project-name]",
        );

        expect(message?.textContent).toBe(
            "Для сохранения сообщения необходимо выбрать проект",
        );
        expect(message).not.toHaveProperty("hidden", true);
        expect(nameInput).toHaveProperty("value", "Рабочий проект");
    });
});