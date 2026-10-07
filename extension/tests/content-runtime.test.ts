/**
 * @vitest-environment jsdom
 */
import { describe, expect, it } from "vitest";
import { runContentScript } from "../src/content-runtime";

describe("runContentScript", () => {
    it("uses the current browser URL and document", () => {
        document.title = "Python discussion";

        const result = runContentScript(
            {
                location: {
                    href: "https://chatgpt.com/c/abc123",
                },
            },
            document,
            () => {},
            () => {},
        );

        expect(result.context).toEqual({
            provider: "chatgpt",
            chatId: "abc123",
            title: "Python discussion",
        });
    });

    it("returns null for unsupported page", () => {
        const result = runContentScript(
            {
                location: {
                    href: "https://example.com/",
                },
            },
            document,
            () => {},
            () => {},
        );

        expect(result).toBeNull();
    });
});