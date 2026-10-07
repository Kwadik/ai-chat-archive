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

    it("saves edited Markdown", () => {
        const onSave = vi.fn();

        const ui = createExtensionUI(
            document,
            context,
            onSave,
            vi.fn(),
        );

        ui.openEditor("Initial");

        const root = document.querySelector(
            "#ai-chat-archive-root",
        ) as HTMLDivElement;

        const textarea = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        textarea.value = "Edited";

        const saveButton = root.shadowRoot?.querySelector(
            "[data-ai-chat-archive-save]",
        ) as HTMLButtonElement;

        saveButton.click();

        expect(onSave).toHaveBeenCalledWith("Edited");
    });

    it("cancels editing", () => {
        const onCancel = vi.fn();

        const ui = createExtensionUI(
            document,
            context,
            vi.fn(),
            onCancel,
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
});