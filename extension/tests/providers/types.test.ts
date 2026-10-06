import { describe, expect, it } from "vitest";
import type { ProviderAdapter } from "../../src/providers/types";

describe("ProviderAdapter", () => {
    it("describes the provider adapter contract", () => {
        const adapter: ProviderAdapter = {
            provider: "chatgpt",

            canHandle(url: URL) {
                return url.hostname === "chatgpt.com";
            },

            getChatId() {
                return null;
            },

            getChatUrl(chatId: string) {
                return `https://chatgpt.com/c/${chatId}`;
            },

            getChatTitle() {
                return null;
            },
        };

        expect(adapter.provider).toBe("chatgpt");
        expect(adapter.canHandle(new URL("https://chatgpt.com/c/test"))).toBe(true);
        expect(adapter.getChatId(new URL("https://chatgpt.com/c/test"))).toBeNull();
        expect(adapter.getChatTitle()).toBeNull();
    });

    it("includes chat URL builder in the provider contract", () => {
        const adapter: ProviderAdapter = {
            provider: "chatgpt",

            canHandle(url: URL) {
                return url.hostname === "chatgpt.com";
            },

            getChatId() {
                return null;
            },

            getChatTitle() {
                return null;
            },

            getChatUrl(chatId: string) {
                return `https://chatgpt.com/c/${chatId}`;
            },
        };

        expect(adapter.getChatUrl("abc123")).toBe(
            "https://chatgpt.com/c/abc123",
        );
    });
});