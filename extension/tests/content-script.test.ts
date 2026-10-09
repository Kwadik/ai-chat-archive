/**
 * @vitest-environment jsdom
 */
import { describe, expect, it, vi } from "vitest";

const runBrowserContentScript = vi.fn();

vi.mock("../src/chat/browser-content-runtime", () => ({
    runBrowserContentScript,
}));

describe("content script", () => {
    it("starts the browser runtime with the local API client", async () => {
        vi.stubGlobal("chrome", {
            storage: {
                local: {
                    get: vi.fn().mockResolvedValue({}),
                    set: vi.fn().mockResolvedValue(undefined),
                },
            },
        });

        await import("../src/content-script");

        expect(runBrowserContentScript).toHaveBeenCalledTimes(1);

        const args = runBrowserContentScript.mock.calls[0];

        expect(args[2]).toBeDefined();
        expect(args[2].constructor.name).toBe(
            "ExtensionApiClient",
        );

        expect(args[3]).toBeNull();
    });

    it("initializes the browser content script with chrome storage and API client", async () => {
        vi.resetModules();

        const chrome = {
            storage: {
                local: {
                    get: vi.fn().mockResolvedValue({}),
                    set: vi.fn().mockResolvedValue(undefined),
                },
            },
        };

        vi.stubGlobal("chrome", chrome);

        const initializeBrowserContentScript = vi.fn();
        const createBrowserApiClient = vi.fn(
            () => "api-client",
        );

        vi.doMock("../src/chat/browser-content-script", () => ({
            initializeBrowserContentScript,
        }));

        vi.doMock("../src/api/browser-api-client", () => ({
            createBrowserApiClient,
        }));

        await import("../src/content-script");

        expect(createBrowserApiClient).toHaveBeenCalledTimes(1);

        expect(
            initializeBrowserContentScript,
        ).toHaveBeenCalledWith(
            chrome,
            "api-client",
            expect.any(Function),
        );
    });
});