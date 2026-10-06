import { describe, expect, it } from "vitest";
import { chatgptProvider } from "../../src/providers/chatgpt";

describe("chatgptProvider", () => {
    it("recognizes ChatGPT URLs", () => {
        expect(
            chatgptProvider.canHandle(
                new URL("https://chatgpt.com/c/abc123"),
            ),
        ).toBe(true);
    });

    it("extracts chat id from a ChatGPT URL", () => {
        expect(
            chatgptProvider.getChatId(
                new URL("https://chatgpt.com/c/abc123"),
            ),
        ).toBe("abc123");
    });

    it("returns null when chat id is missing", () => {
        expect(
            chatgptProvider.getChatId(
                new URL("https://chatgpt.com/"),
            ),
        ).toBeNull();
    });

    it("reads chat title from the document", () => {
        const document = {
            title: "Python discussion",
        };

        expect(chatgptProvider.getChatTitle(document)).toBe(
            "Python discussion",
        );
    });

    it("returns null when chat title is empty", () => {
        const document = {
            title: "   ",
        };

        expect(chatgptProvider.getChatTitle(document)).toBeNull();
    });

    it("extracts chat id when URL has query parameters", () => {
        expect(
            chatgptProvider.getChatId(
                new URL("https://chatgpt.com/c/abc123?foo=bar"),
            ),
        ).toBe("abc123");
    });

    it("returns null for a non-chat ChatGPT path", () => {
        expect(
            chatgptProvider.getChatId(
                new URL("https://chatgpt.com/gpts"),
            ),
        ).toBeNull();
    });

    it("rejects non-ChatGPT hosts", () => {
        expect(
            chatgptProvider.canHandle(
                new URL("https://example.com/c/abc123"),
            ),
        ).toBe(false);
    });

    it("rejects ChatGPT subdomains", () => {
        expect(
            chatgptProvider.canHandle(
                new URL("https://www.chatgpt.com/c/abc123"),
            ),
        ).toBe(false);
    });

    it("uses the ChatGPT URL parser to extract chat id", () => {
        const url = new URL(
            "https://chatgpt.com/c/abc123?foo=bar",
        );

        expect(chatgptProvider.getChatId(url)).toBe("abc123");
    });

    it("builds ChatGPT chat URL", () => {
        expect(
            chatgptProvider.getChatUrl("abc123"),
        ).toBe("https://chatgpt.com/c/abc123");
    });
});