/**
 * @vitest-environment jsdom
 */
import { describe, expect, it, vi } from "vitest";
import { runBrowserContentScript } from "../../src/chat/browser-content-runtime";
import type { ExtensionApiClient } from "../../src/api/api-client";
import type { ExtensionUIOptions } from "../../src/ui/extension-ui";

describe("runBrowserContentScript", () => {
    it("uses the browser window location and document", () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/abc123",
            },
        });

        document.title = "Python discussion";

        const result = runBrowserContentScript();

        expect(result!.context).toEqual({
            provider: "chatgpt",
            chatId: "abc123",
            title: "Python discussion",
        });

        vi.unstubAllGlobals();
    });

    it("creates the extension UI for the current browser chat", () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/chat-123",
            },
        });

        document.title = "Test chat";

        const ui = runBrowserContentScript();

        expect(ui).toBeDefined();
        expect(ui!.context).toEqual({
            provider: "chatgpt",
            chatId: "chat-123",
            title: "Test chat",
        });

        vi.unstubAllGlobals();
    });

    it("passes the browser clipboard to the content UI", async () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/chat-123",
            },
        });

        document.title = "Test chat";

        const clipboard = {
            readText: vi.fn().mockResolvedValue(
                "Copied **Markdown**",
            ),
        };

        vi.stubGlobal("navigator", {
            clipboard,
        });

        const ui = runBrowserContentScript();

        expect(ui).toBeDefined();

        await ui!.openEditorFromClipboard();

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const textarea = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        expect(textarea.value).toBe("Copied **Markdown**");

        vi.unstubAllGlobals();
    });

    it("passes saved Markdown and chat context to the save callback", () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/chat-123",
            },
        });

        document.title = "Test chat";

        const onSave = vi.fn();

        const ui = runBrowserContentScript(
            onSave,
            () => {},
        );

        expect(ui).toBeDefined();

        ui!.openEditor("Initial Markdown");

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const textarea = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        textarea.value = "Saved **Markdown**";

        const saveButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-save]",
        ) as HTMLButtonElement;

        saveButton.click();

        expect(onSave).toHaveBeenCalledWith(
            "Saved **Markdown**",
            {
                provider: "chatgpt",
                chatId: "chat-123",
                title: "Test chat",
            },
        );

        vi.unstubAllGlobals();
    });

    it("saves edited Markdown through the API client", async () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/chat-123",
            },
        });

        document.title = "Test chat";

        const apiClient = {
            createMessage: vi.fn().mockResolvedValue({
                number: 1,
                role: "user",
                file_name: "001-user.md",
            }),
        } as unknown as ExtensionApiClient;

        const onSave = vi.fn();

        const uiOptions: Omit<ExtensionUIOptions, "selectedProjectId"> & {
            selectedProjectId: string | null;
        } = {
            selectedProjectId: null,
            createProject: vi.fn(),
            listProjects: vi.fn(),
            saveSelectedProjectId: vi.fn(),
        };

        const ui = runBrowserContentScript(
            onSave,
            () => {},
            apiClient,
            null,
            uiOptions,
        );

        expect(ui).not.toBeNull();

        ui!.openEditor("Original Markdown");

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const saveButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-save]",
        ) as HTMLButtonElement;

        uiOptions.selectedProjectId = "new-project";

        saveButton.click();

        expect(apiClient.createMessage).toHaveBeenCalledWith({
            projectId: "new-project",
            provider: "chatgpt",
            chatId: "chat-123",
            role: "user",
            content: "Original Markdown",
        });

        vi.unstubAllGlobals();
    });

    it("uses the provided project when saving", () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/chat-123",
            },
        });

        document.title = "Test chat";

        const apiClient = {
            createMessage: vi.fn().mockResolvedValue({
                number: 1,
                role: "user",
                file_name: "001-user.md",
            }),
        } as unknown as ExtensionApiClient;

        const ui = runBrowserContentScript(
            () => {},
            () => {},
            apiClient,
            "project-python",
        );

        expect(ui).toBeDefined();

        ui!.openEditor("Python Markdown");

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const saveButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-save]",
        ) as HTMLButtonElement;

        saveButton.click();

        expect(apiClient.createMessage).toHaveBeenCalledWith({
            projectId: "project-python",
            provider: "chatgpt",
            chatId: "chat-123",
            role: "user",
            content: "Python Markdown",
        });

        vi.unstubAllGlobals();
    });

    it("uses the provided API client when saving", () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/chat-123",
            },
        });

        document.title = "Test chat";

        const apiClient = {
            createMessage: vi.fn().mockResolvedValue({
                number: 1,
                role: "user",
                file_name: "001-user.md",
            }),
        } as unknown as ExtensionApiClient;

        const ui = runBrowserContentScript(
            () => {},
            () => {},
            apiClient,
        );

        expect(ui).toBeDefined();

        vi.unstubAllGlobals();
    });

    it("does not save through the API when no project is selected", () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/chat-123",
            },
        });

        document.title = "Test chat";

        const apiClient = {
            createMessage: vi.fn().mockResolvedValue({
                number: 1,
                role: "user",
                file_name: "001-user.md",
            }),
        } as unknown as ExtensionApiClient;

        const ui = runBrowserContentScript(
            () => {},
            () => {},
            apiClient,
            null,
        );

        expect(ui).toBeDefined();

        ui!.openEditor("Some Markdown");

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const saveButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-save]",
        ) as HTMLButtonElement;

        saveButton.click();

        expect(apiClient.createMessage).not.toHaveBeenCalled();

        vi.unstubAllGlobals();
    });
});