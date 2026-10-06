import { describe, expect, it, vi } from "vitest";
import { runBrowserContentScript } from "../src/browser-content-runtime";

describe("runBrowserContentScript", () => {
    it("uses the browser window location and document", () => {
        vi.stubGlobal("window", {
            location: {
                href: "https://chatgpt.com/c/abc123",
            },
        });

        vi.stubGlobal("document", {
            title: "Python discussion",
        });

        const result = runBrowserContentScript();

        expect(result?.provider).toBe("chatgpt");
        expect(result?.chatId).toBe("abc123");
        expect(result?.title).toBe("Python discussion");

        vi.unstubAllGlobals();
    });
});