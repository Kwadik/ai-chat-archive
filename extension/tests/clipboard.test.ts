import { describe, expect, it, vi } from "vitest";
import { readMarkdownFromClipboard } from "../src/clipboard";

describe("clipboard", () => {
    it("reads Markdown text from clipboard", async () => {
        const clipboard = {
            readText: vi.fn().mockResolvedValue(
                "# Hello\n\nThis is **Markdown**.",
            ),
        };

        const result = await readMarkdownFromClipboard(clipboard);

        expect(result).toBe(
            "# Hello\n\nThis is **Markdown**.",
        );

        expect(clipboard.readText).toHaveBeenCalledTimes(1);
    });

    it("returns null when clipboard is unavailable", async () => {
        const result = await readMarkdownFromClipboard(null);

        expect(result).toBeNull();
    });

    it("returns null when clipboard read fails", async () => {
        const clipboard = {
            readText: vi.fn().mockRejectedValue(
                new Error("Clipboard permission denied"),
            ),
        };

        const result = await readMarkdownFromClipboard(clipboard);

        expect(result).toBeNull();
    });
});