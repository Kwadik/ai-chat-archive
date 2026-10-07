/**
 * @vitest-environment jsdom
 */
import {
    describe,
    expect,
    it,
    vi,
} from "vitest";
import { createExtensionRoot } from "../src/extension-root";
import {
    createExtensionPanel,
    showExtensionEditor,
} from "../src/extension-panel";

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

    it("closes the panel when the close button is clicked", () => {
        const root = createExtensionRoot(document);
        const panel = createExtensionPanel(root);

        const closeButton = panel.querySelector(
            "[data-ai-chat-archive-close]",
        );

        expect(panel.hidden).toBe(false);

        (closeButton as HTMLButtonElement).click();

        expect(panel.hidden).toBe(true);
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
});