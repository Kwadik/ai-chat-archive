import { describe, expect, it, vi } from "vitest";

const runBrowserContentScript = vi.fn();

vi.mock("../src/browser-content-runtime", () => ({
    runBrowserContentScript,
}));

describe("content script", () => {
    it("starts the browser runtime with the local API client", async () => {
        await import("../src/content-script");

        expect(runBrowserContentScript).toHaveBeenCalledTimes(1);

        const apiClient =
            runBrowserContentScript.mock.calls[0][2];

        expect(apiClient).toBeDefined();
        expect(apiClient.constructor.name).toBe(
            "ExtensionApiClient",
        );
    });
});