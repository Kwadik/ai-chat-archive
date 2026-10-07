/**
 * @vitest-environment jsdom
 */
import { describe, expect, it, vi } from "vitest";
import {
    createExtensionEditor,
} from "../src/extension-editor";

describe("extension editor", () => {
    it("creates a Markdown textarea", () => {
        const onSave = vi.fn();
        const onCancel = vi.fn();

        const editor = createExtensionEditor(
            "Initial **Markdown**",
            onSave,
            onCancel,
        );

        const textarea = editor.querySelector(
            "[data-ai-chat-archive-editor]",
        );

        expect(textarea).not.toBeNull();
        expect(textarea?.tagName).toBe("TEXTAREA");
        expect(
            (textarea as HTMLTextAreaElement).value,
        ).toBe("Initial **Markdown**");
    });

    it("provides a Save button", () => {
        const editor = createExtensionEditor(
            "",
            vi.fn(),
            vi.fn(),
        );

        const saveButton = editor.querySelector(
            "[data-ai-chat-archive-save]",
        );

        expect(saveButton).not.toBeNull();
        expect(saveButton?.textContent).toBe("Save");
    });

    it("provides a Cancel button", () => {
        const editor = createExtensionEditor(
            "",
            vi.fn(),
            vi.fn(),
        );

        const cancelButton = editor.querySelector(
            "[data-ai-chat-archive-cancel]",
        );

        expect(cancelButton).not.toBeNull();
        expect(cancelButton?.textContent).toBe("Cancel");
    });

    it("passes the current Markdown to onSave", () => {
        const onSave = vi.fn();

        const editor = createExtensionEditor(
            "Initial",
            onSave,
            vi.fn(),
        );

        const textarea = editor.querySelector(
            "[data-ai-chat-archive-editor]",
        ) as HTMLTextAreaElement;

        textarea.value = "Edited **Markdown**";

        const saveButton = editor.querySelector(
            "[data-ai-chat-archive-save]",
        ) as HTMLButtonElement;

        saveButton.click();

        expect(onSave).toHaveBeenCalledWith(
            "Edited **Markdown**",
        );
    });

    it("calls onCancel when Cancel is clicked", () => {
        const onCancel = vi.fn();

        const editor = createExtensionEditor(
            "Initial",
            vi.fn(),
            onCancel,
        );

        const cancelButton = editor.querySelector(
            "[data-ai-chat-archive-cancel]",
        ) as HTMLButtonElement;

        cancelButton.click();

        expect(onCancel).toHaveBeenCalledTimes(1);
    });
});