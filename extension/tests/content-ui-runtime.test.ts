/**
 * @vitest-environment jsdom
 */
import { describe, expect, it, vi } from "vitest";
import { initializeContentUI } from "../src/content-ui-runtime";

describe("content UI runtime", () => {
    it("creates UI for the current ChatGPT chat", () => {
        const ui = initializeContentUI(
            document,
            new URL("https://chatgpt.com/c/chat-123"),
            vi.fn(),
            vi.fn(),
        );

        expect(ui.context).toEqual({
            provider: "chatgpt",
            chatId: "chat-123",
            title: null,
        });
    });
});