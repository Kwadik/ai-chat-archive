/**
 * @vitest-environment jsdom
 */
import { describe, expect, it, vi } from "vitest";
import {
    createExtensionUI,
} from "../src/extension-ui";
import type { ChatContext } from "../src/chat-context";

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
});