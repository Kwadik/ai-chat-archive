import { describe, expect, it } from "vitest";
import {
    getCurrentChatContext,
    getCurrentChatId,
    getCurrentChatTitle,
    getCurrentChatUrl,
    getCurrentProvider,
} from "../src/content";

describe("getCurrentProvider", () => {
    it("returns ChatGPT provider for ChatGPT URL", () => {
        const provider = getCurrentProvider(
            new URL("https://chatgpt.com/c/abc123"),
        );

        expect(provider?.provider).toBe("chatgpt");
    });

    it("returns null for unsupported URL", () => {
        const provider = getCurrentProvider(
            new URL("https://example.com/"),
        );

        expect(provider).toBeNull();
    });

    it("returns chat id for supported ChatGPT URL", () => {
        const chatId = getCurrentChatId(
            new URL("https://chatgpt.com/c/abc123"),
        );

        expect(chatId).toBe("abc123");
    });

    it("returns null for unsupported URL", () => {
        const chatId = getCurrentChatId(
            new URL("https://example.com/"),
        );

        expect(chatId).toBeNull();
    });

    it("returns chat title for supported ChatGPT URL", () => {
        const title = getCurrentChatTitle(
            new URL("https://chatgpt.com/c/abc123"),
            {
                title: "Python discussion",
            },
        );

        expect(title).toBe("Python discussion");
    });

    it("returns null for unsupported URL", () => {
        const title = getCurrentChatTitle(
            new URL("https://example.com/"),
            {
                title: "Python discussion",
            },
        );

        expect(title).toBeNull();
    });

    it("returns current chat context", () => {
        const context = getCurrentChatContext(
            new URL("https://chatgpt.com/c/abc123"),
            {
                title: "Python discussion",
            },
        );

        expect(context).toEqual({
            provider: "chatgpt",
            chatId: "abc123",
            title: "Python discussion",
        });
    });

    it("returns null when chat id is missing", () => {
        const context = getCurrentChatContext(
            new URL("https://chatgpt.com/"),
            {
                title: "Python discussion",
            },
        );

        expect(context).toBeNull();
    });

    it("returns current chat URL", () => {
        const chatUrl = getCurrentChatUrl(
            new URL("https://chatgpt.com/c/abc123"),
        );

        expect(chatUrl).toBe(
            "https://chatgpt.com/c/abc123",
        );
    });

    it("returns null for a page without a chat", () => {
        const chatUrl = getCurrentChatUrl(
            new URL("https://chatgpt.com/"),
        );

        expect(chatUrl).toBeNull();
    });
});