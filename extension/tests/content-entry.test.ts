import { describe, expect, it } from "vitest";
import { initializeContentScript } from "../src/content-entry";

describe("initializeContentScript", () => {
    it("returns current chat context", () => {
        const context = initializeContentScript(
            new URL("https://chatgpt.com/c/abc123"),
            {
                title: "Python discussion",
            },
        );

        expect(context?.provider).toBe("chatgpt");
        expect(context?.chatId).toBe("abc123");
        expect(context?.title).toBe("Python discussion");
    });

    it("returns null for unsupported page", () => {
        const context = initializeContentScript(
            new URL("https://example.com/"),
            {
                title: "Example",
            },
        );

        expect(context).toBeNull();
    });
});