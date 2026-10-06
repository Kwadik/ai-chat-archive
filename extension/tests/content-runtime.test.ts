import { describe, expect, it } from "vitest";
import { runContentScript } from "../src/content-runtime";

describe("runContentScript", () => {
    it("uses the current browser URL and document", () => {
        const result = runContentScript({
            location: {
                href: "https://chatgpt.com/c/abc123",
            },
            document: {
                title: "Python discussion",
            },
        });

        expect(result?.provider).toBe("chatgpt");
        expect(result?.chatId).toBe("abc123");
        expect(result?.title).toBe("Python discussion");
    });

    it("returns null for unsupported page", () => {
        const result = runContentScript({
            location: {
                href: "https://example.com/",
            },
            document: {
                title: "Example",
            },
        });

        expect(result).toBeNull();
    });
});