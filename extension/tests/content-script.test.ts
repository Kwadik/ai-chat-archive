import { describe, expect, it, vi } from "vitest";

const runBrowserContentScript = vi.fn();

vi.mock("../src/browser-content-runtime", () => ({
    runBrowserContentScript,
}));

describe("content script", () => {
    it("starts browser content runtime", async () => {
        await import("../src/content-script");

        expect(runBrowserContentScript).toHaveBeenCalledOnce();
    });
});