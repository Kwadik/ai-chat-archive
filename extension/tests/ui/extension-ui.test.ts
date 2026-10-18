/**
 * @vitest-environment jsdom
 */
import { describe, expect, it, vi } from "vitest";
import {
    createExtensionUI,
} from "../../src/ui/extension-ui";
import type { ChatContext } from "../../src/chat/chat-context";

describe("extension UI", () => {
    const context: ChatContext = {
        provider: "chatgpt",
        chatId: "chat-123",
        title: null,
    };

    it("opens the editor with initial Markdown", () => {
        const onSave = vi.fn();
        const onCancel = vi.fn();

        const ui = createExtensionUI(
            document,
            context,
            onSave,
            onCancel,
            null,
        );

        ui.openEditor("Hello **world**");

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const textarea = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        expect(textarea).not.toBeNull();
        expect(textarea.value).toBe("Hello **world**");
    });

    it("passes Markdown and chat context to the save callback", () => {
        const onSave = vi.fn();
        const onCancel = vi.fn();

        const context: ChatContext = {
            provider: "chatgpt",
            chatId: "chat-123",
            title: "Test chat",
        };

        const ui = createExtensionUI(
            document,
            context,
            onSave,
            onCancel,
            null,
        );

        ui.openEditor("Edited **Markdown**");

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const textarea = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        textarea.value = "Updated content";

        const saveButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-save]",
        ) as HTMLButtonElement;

        saveButton.click();

        expect(onSave).toHaveBeenCalledWith(
            "Updated content",
            context,
        );
    });

    it("cancels editing", () => {
        const onCancel = vi.fn();

        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            onCancel,
            null,
        );

        ui.openEditor("Initial");

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const cancelButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-cancel]",
        ) as HTMLButtonElement;

        cancelButton.click();

        expect(onCancel).toHaveBeenCalledTimes(1);
    });

    it("closes the editor when the panel close button is clicked", () => {
        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            null,
        );

        ui.openEditor("Initial");

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const closeButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-close]",
        ) as HTMLButtonElement;

        const panel = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-panel]",
        ) as HTMLDivElement;

        closeButton.click();

        expect(panel.hidden).toBe(true);
    });

    it("opens the editor with Markdown from clipboard", async () => {
        const onSave = vi.fn();
        const onCancel = vi.fn();

        const context: ChatContext = {
            provider: "chatgpt",
            chatId: "chat-123",
            title: null,
        };

        const clipboard = {
            readText: vi.fn().mockResolvedValue(
                "Copied **Markdown**",
            ),
        };

        const ui = createExtensionUI(
            document,
            context,
            onSave,
            onCancel,
            clipboard,
        );

        await ui.openEditorFromClipboard();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const textarea = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        expect(textarea.value).toBe("Copied **Markdown**");
    });

    it("opens an empty editor when clipboard is unavailable", async () => {
        const onSave = vi.fn();
        const onCancel = vi.fn();

        const context: ChatContext = {
            provider: "chatgpt",
            chatId: "chat-123",
            title: null,
        };

        const ui = createExtensionUI(
            document,
            context,
            onSave,
            onCancel,
            null,
        );

        await ui.openEditorFromClipboard();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const textarea = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        expect(textarea.value).toBe("");
    });

    it("shows project creation instead of opening the editor when no project is selected", async () => {
        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            null,
            {
                selectedProjectId: null,
                createProject: vi.fn(),
                listProjects: vi.fn().mockResolvedValue([]),
            },
        );

        await ui.openEditorFromClipboard();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const shadow = root.shadowRoot;

        expect(
            shadow?.querySelector("[data-ai-chat-archive-editor]"),
        ).toBeNull();

        expect(
            shadow?.querySelector("[data-ai-chat-archive-create-project]"),
        ).not.toBeNull();

        const nameInput = shadow?.querySelector(
            "[data-ai-chat-archive-project-name]",
        ) as HTMLInputElement;

        expect(nameInput.value).toBe("Мой проект");
    });

    it("shows project selection when projects exist but none is selected", async () => {
        const listProjects = vi.fn().mockResolvedValue([
            { id: "project-1", name: "Рабочий проект" },
            { id: "project-2", name: "Личный проект" },
        ]);

        const options = {
            selectedProjectId: null,
            createProject: vi.fn(),
            listProjects,
        };

        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            null,
            options,
        );

        await ui.openEditorFromClipboard();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const shadow = root.shadowRoot;

        expect(listProjects).toHaveBeenCalledOnce();

        expect(
            shadow?.querySelector("[data-ai-chat-archive-project-selector]"),
        ).not.toBeNull();

        expect(shadow?.textContent).toContain("Рабочий проект");
        expect(shadow?.textContent).toContain("Личный проект");

        expect(
            shadow?.querySelector("[data-ai-chat-archive-create-project]"),
        ).not.toBeNull();
    });

    it("creates a project when the project creation form is submitted", async () => {
        const createProject = vi.fn().mockResolvedValue({
            id: "new-project",
            name: "Рабочий проект",
        });

        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            null,
            {
                selectedProjectId: null,
                createProject,
                listProjects: vi.fn().mockResolvedValue([]),
            },
        );

        await ui.openEditorFromClipboard();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const shadow = root.shadowRoot;

        const nameInput = shadow?.querySelector(
            "[data-ai-chat-archive-project-name]",
        ) as HTMLInputElement;

        const form = shadow?.querySelector(
            "[data-ai-chat-archive-create-project]",
        ) as HTMLFormElement;

        nameInput.value = "Рабочий проект";
        form.dispatchEvent(
            new Event("submit", { bubbles: true, cancelable: true }),
        );

        await Promise.resolve();

        expect(createProject).toHaveBeenCalledWith("Рабочий проект");
    });

    it("opens the editor after creating a project", async () => {
        const createProject = vi.fn().mockResolvedValue({
            id: "new-project",
            name: "Рабочий проект",
        });

        const saveSelectedProjectId = vi.fn().mockResolvedValue(undefined);

        const clipboard = {
            readText: vi.fn().mockResolvedValue("# Скопированное сообщение"),
        };

        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            clipboard,
            {
                selectedProjectId: null,
                createProject,
                listProjects: vi.fn().mockResolvedValue([]),
                saveSelectedProjectId,
            },
        );

        await ui.openEditorFromClipboard();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const shadow = root.shadowRoot;

        const nameInput = shadow?.querySelector(
            "[data-ai-chat-archive-project-name]",
        ) as HTMLInputElement;

        const form = shadow?.querySelector(
            "[data-ai-chat-archive-create-project]",
        ) as HTMLFormElement;

        nameInput.value = "Рабочий проект";
        form.dispatchEvent(
            new Event("submit", { bubbles: true, cancelable: true }),
        );

        await vi.waitFor(() => {
            expect(
                shadow?.querySelector("[data-ai-chat-archive-editor]"),
            ).not.toBeNull();
        });

        expect(
            shadow?.querySelector<HTMLTextAreaElement>(
                "[data-ai-chat-archive-editor]",
            )?.value,
        ).toBe("# Скопированное сообщение");

        expect(saveSelectedProjectId).toHaveBeenCalledWith("new-project");
    });

    it("opens the editor after selecting an existing project", async () => {
        const listProjects = vi.fn().mockResolvedValue([
            { id: "project-1", name: "Рабочий проект" },
            { id: "project-2", name: "Личный проект" },
        ]);
        const saveSelectedProjectId = vi.fn().mockResolvedValue(undefined);

        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            {
                readText: vi.fn().mockResolvedValue("# Сообщение"),
            },
            {
                selectedProjectId: null,
                createProject: vi.fn(),
                listProjects,
                saveSelectedProjectId,
            },
        );

        await ui.openEditorFromClipboard();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;
        const shadow = root.shadowRoot;

        const projectButton = Array.from(
            shadow?.querySelectorAll("button") ?? [],
        ).find((button) => button.textContent === "Рабочий проект");

        expect(projectButton).toBeDefined();

        projectButton?.click();

        await vi.waitFor(() => {
            expect(
                shadow?.querySelector("[data-ai-chat-archive-editor]"),
            ).not.toBeNull();
        });

        expect(saveSelectedProjectId).toHaveBeenCalledWith("project-1");

        expect(
            shadow?.querySelector<HTMLTextAreaElement>(
                "[data-ai-chat-archive-editor]",
            )?.value,
        ).toBe("# Сообщение");
    });

    it("opens the home screen and displays the selected project", async () => {
        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            null,
            {
                selectedProjectId: "project-1",
                createProject: vi.fn(),
                listProjects: vi.fn().mockResolvedValue([
                    { id: "project-1", name: "Рабочий проект" },
                ]),
            },
        );

        await ui.openHome();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const shadow = root.shadowRoot;

        expect(
            shadow?.querySelector("[data-ai-chat-archive-home]"),
        ).not.toBeNull();

        expect(shadow?.textContent).toContain("Рабочий проект");
    });

    it("returns to the home screen after selecting a project", async () => {
        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            null,
            {
                selectedProjectId: null,
                createProject: vi.fn(),
                listProjects: vi.fn().mockResolvedValue([
                    { id: "project-1", name: "Рабочий проект" },
                ]),
            },
        );

        await ui.openHome();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const shadow = root.shadowRoot;

        const showProjectsButton = shadow?.querySelector(
            "[data-ai-chat-archive-show-projects]",
        ) as HTMLButtonElement;

        showProjectsButton.click();

        await vi.waitFor(() => {
            expect(
                shadow?.querySelector("[data-ai-chat-archive-project-selector]"),
            ).not.toBeNull();
        });

        const projectButton = Array.from(
            shadow?.querySelectorAll("button") ?? [],
        ).find((button) => button.textContent?.includes("Рабочий проект"));

        expect(projectButton).toBeDefined();

        projectButton?.click();

        await Promise.resolve();
        await Promise.resolve();

        expect(
            shadow?.querySelector("[data-ai-chat-archive-home]"),
        ).not.toBeNull();

        expect(shadow?.textContent).toContain("Рабочий проект");
    });

    it("creates a project from the home screen and selects it", async () => {
        const createProject = vi.fn().mockResolvedValue({
            id: "project-2",
            name: "Новый проект",
        });
        const saveSelectedProjectId = vi.fn().mockResolvedValue(undefined);
        const listProjects = vi.fn()
            .mockResolvedValueOnce([])
            .mockResolvedValueOnce([
                { id: "project-2", name: "Новый проект" },
            ]);

        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            null,
            {
                selectedProjectId: null,
                createProject,
                listProjects,
                saveSelectedProjectId,
            },
        );

        await ui.openHome();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;
        const shadow = root.shadowRoot;

        const createButton = Array.from(
            shadow?.querySelectorAll("button") ?? [],
        ).find((button) => button.textContent?.includes("Создать проект"));

        expect(createButton).toBeDefined();
        createButton?.click();

        const input = shadow?.querySelector(
            "[data-ai-chat-archive-project-name]",
        ) as HTMLInputElement;

        input.value = "Новый проект";

        const form = shadow?.querySelector(
            "[data-ai-chat-archive-create-project]",
        ) as HTMLFormElement;

        form.requestSubmit();

        await vi.waitFor(() => {
            expect(createProject).toHaveBeenCalledWith("Новый проект");
            expect(saveSelectedProjectId).toHaveBeenCalledWith("project-2");
        });

        expect(
            shadow?.querySelector("[data-ai-chat-archive-home]"),
        ).not.toBeNull();
        expect(shadow?.textContent).toContain("Новый проект");
    });

    it("creates a project from project selection and opens the editor", async () => {
        const createProject = vi.fn().mockResolvedValue({
            id: "project-2",
            name: "Новый проект",
        });

        const listProjects = vi.fn()
            .mockResolvedValueOnce([
                { id: "project-1", name: "Рабочий проект" },
            ])
            .mockResolvedValueOnce([
                { id: "project-1", name: "Рабочий проект" },
            ])
            .mockResolvedValueOnce([
                { id: "project-2", name: "Новый проект" },
            ]);

        const saveSelectedProjectId = vi.fn().mockResolvedValue(undefined);

        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            vi.fn(),
            null,
            {
                selectedProjectId: null,
                createProject,
                listProjects,
                saveSelectedProjectId,
            },
        );

        await ui.openHome();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;
        const shadow = root.shadowRoot;

        const showProjectsButton = Array.from(
            shadow?.querySelectorAll("button") ?? [],
        ).find((button) => button.textContent?.includes("Все проекты"));

        showProjectsButton?.click();

        await vi.waitFor(() => {
            expect(
                shadow?.querySelector("[data-ai-chat-archive-project-selector]"),
            ).not.toBeNull();
        });

        const createButton = shadow?.querySelector(
            "[data-ai-chat-archive-create-project]",
        ) as HTMLButtonElement;

        createButton.click();

        const input = shadow?.querySelector(
            "[data-ai-chat-archive-project-name]",
        ) as HTMLInputElement;

        input.value = "Новый проект";

        const form = shadow?.querySelector(
            "form[data-ai-chat-archive-create-project]",
        ) as HTMLFormElement;

        expect(form).not.toBeNull();

        form.requestSubmit();

        await vi.waitFor(() => {
            expect(createProject).toHaveBeenCalledWith("Новый проект");
            expect(saveSelectedProjectId).toHaveBeenCalledWith("project-2");
        });

        await vi.waitFor(() => {
            expect(
                shadow?.querySelector("[data-ai-chat-archive-home]"),
            ).not.toBeNull();

            expect(
                shadow?.querySelector(
                    "[data-ai-chat-archive-current-project-name]",
                )?.textContent,
            ).toContain("Новый проект");
        });
    });
});