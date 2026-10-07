import { describe, expect, it, vi } from "vitest";
import {
    getSelectedProjectId,
    setSelectedProjectId,
} from "../src/project-config";

describe("project config", () => {
    it("returns the default project when storage is empty", async () => {
        const storage = {
            local: {
                get: vi.fn().mockResolvedValue({}),
                set: vi.fn().mockResolvedValue(undefined),
            },
        };

        const projectId = await getSelectedProjectId(
            storage,
        );

        expect(projectId).toBe("default");
    });

    it("stores and returns the selected project", async () => {
        const storage = {
            local: {
                get: vi.fn().mockResolvedValue({
                    selectedProjectId: "project-python",
                }),
                set: vi.fn().mockResolvedValue(undefined),
            },
        };

        await setSelectedProjectId(
            "project-python",
            storage,
        );

        expect(storage.local.set).toHaveBeenCalledWith({
            selectedProjectId: "project-python",
        });

        const projectId = await getSelectedProjectId(
            storage,
        );

        expect(projectId).toBe("project-python");
    });

    it("reads the selected project from browser storage", async () => {
        const storage = {
            local: {
                get: async () => ({
                    selectedProjectId: "project-browser",
                }),
                set: async () => {},
            },
        };

        const chrome = {
            storage,
        };

        const projectId = await getSelectedProjectId(
            chrome.storage,
        );

        expect(projectId).toBe("project-browser");
    });
});