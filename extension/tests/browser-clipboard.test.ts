import { describe, expect, it, vi } from "vitest";
import { readBrowserClipboard } from "../src/browser-clipboard";

describe("browser clipboard", () => {
    it("reads Markdown from the browser clipboard", async () => {
        const clipboard = {
            readText: vi.fn().mockResolvedValue(
                "Hello **world**",
            ),
        };

        const result = await readBrowserClipboard(clipboard);

        expect(result).toBe("Hello **world**");
        expect(clipboard.readText).toHaveBeenCalledTimes(1);
    });
});