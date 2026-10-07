/**
 * @vitest-environment jsdom
 */
import { describe, expect, it, vi } from "vitest";
import { createContentUI } from "../src/content-ui";

describe("content UI", () => {
    it("opens the editor through the extension UI", () => {
        const ui = createContentUI(
            document,
            vi.fn(),
            vi.fn(),
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
});