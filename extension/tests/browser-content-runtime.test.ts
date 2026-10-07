/**
 * @vitest-environment jsdom
 */
import { describe, expect, it, vi } from "vitest";
import { runBrowserContentScript } from "../src/browser-content-runtime";

describe("runBrowserContentScript", () => {
    it("uses the browser window location and document", () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/abc123",
            },
        });

        document.title = "Python discussion";

        const result = runBrowserContentScript();

        expect(result.context).toEqual({
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
        expect(ui.context).toEqual({
            provider: "chatgpt",
            chatId: "chat-123",
            title: "Test chat",
        });

        vi.unstubAllGlobals();
    });
});