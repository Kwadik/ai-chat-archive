import { describe, expect, it, vi } from "vitest";
import type { ExtensionApiClient } from "../../src/api/api-client";

describe("initializeBrowserContentScript", () => {
    it("loads the selected project from browser storage", async () => {
        const storage = {
            local: {
                get: vi.fn().mockResolvedValue({
                    selectedProjectId: "project-browser",
                }),
                set: vi.fn().mockResolvedValue(undefined),
            },
        };

        const chrome = {
            storage,
        };

        const apiClient = {} as ExtensionApiClient;
        const runBrowserContentScript = vi.fn();

        const { initializeBrowserContentScript } = await import(
            "../../src/chat/browser-content-script"
            );

        await initializeBrowserContentScript(
            chrome,
            apiClient,
            runBrowserContentScript,
        );

        expect(runBrowserContentScript).toHaveBeenCalledWith(
            expect.any(Function),
            expect.any(Function),
            apiClient,
            "project-browser",
            expect.objectContaining({
                selectedProjectId: "project-browser",
                listProjects: expect.any(Function),
                createProject: expect.any(Function),
                saveSelectedProjectId: expect.any(Function),
            }),
        );
    });

    it("passes the API client to the browser content runtime", async () => {
        const storage = {
            local: {
                get: vi.fn().mockResolvedValue({
                    selectedProjectId: "project-browser",
                }),
                set: vi.fn().mockResolvedValue(undefined),
            },
        };

        const chrome = {
            storage,
        };

        const apiClient = {} as ExtensionApiClient;
        const runBrowserContentScript = vi.fn();

        const { initializeBrowserContentScript } = await import(
            "../../src/chat/browser-content-script"
            );

        await initializeBrowserContentScript(
            chrome,
            apiClient,
            runBrowserContentScript,
        );

        expect(runBrowserContentScript).toHaveBeenCalledWith(
            expect.any(Function),
            expect.any(Function),
            apiClient,
            "project-browser",
            expect.objectContaining({
                selectedProjectId: "project-browser",
                listProjects: expect.any(Function),
                createProject: expect.any(Function),
                saveSelectedProjectId: expect.any(Function),
            }),
        );
    });

    it("passes null when no project is selected", async () => {
        const storage = {
            local: {
                get: vi.fn().mockResolvedValue({}),
                set: vi.fn().mockResolvedValue(undefined),
            },
        };

        const chrome = { storage };
        const apiClient = {
            listProjects: vi.fn().mockResolvedValue([]),
        } as unknown as ExtensionApiClient;
        const runBrowserContentScript = vi.fn();

        const { initializeBrowserContentScript } = await import(
            "../../src/chat/browser-content-script"
            );

        await initializeBrowserContentScript(
            chrome,
            apiClient,
            runBrowserContentScript,
        );

        expect(runBrowserContentScript).toHaveBeenCalledWith(
            expect.any(Function),
            expect.any(Function),
            apiClient,
            null,
            expect.objectContaining({
                selectedProjectId: null,
                listProjects: expect.any(Function),
                createProject: expect.any(Function),
                saveSelectedProjectId: expect.any(Function),
            }),
        );
    });
});