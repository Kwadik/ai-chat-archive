import { describe, expect, it } from "vitest";
import { getChatIdFromChatGPTUrl } from "../../src/providers/chatgpt-url";

describe("getChatIdFromChatGPTUrl", () => {
    it("extracts chat id", () => {
        expect(
            getChatIdFromChatGPTUrl(
                new URL("https://chatgpt.com/c/abc123"),
            ),
        ).toBe("abc123");
    });

    it("ignores query parameters", () => {
        expect(
            getChatIdFromChatGPTUrl(
                new URL("https://chatgpt.com/c/abc123?foo=bar"),
            ),
        ).toBe("abc123");
    });

    it("returns null for a non-chat path", () => {
        expect(
            getChatIdFromChatGPTUrl(
                new URL("https://chatgpt.com/gpts"),
            ),
        ).toBeNull();
    });

    it("returns null when chat id is missing", () => {
        expect(
            getChatIdFromChatGPTUrl(
                new URL("https://chatgpt.com/c/"),
            ),
        ).toBeNull();
    });

    it("returns null for a nested chat path", () => {
        expect(
            getChatIdFromChatGPTUrl(
                new URL("https://chatgpt.com/c/abc123/messages"),
            ),
        ).toBeNull();
    });
});