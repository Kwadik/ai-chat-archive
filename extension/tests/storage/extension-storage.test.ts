import { describe, expect, it, vi } from "vitest";
import {
    getStoredProjectId,
    setStoredProjectId,
} from "../../src/storage/extension-storage";

describe("extension storage", () => {
    it("stores and reads the selected project", async () => {
        const storage = {
            local: {
                get: vi.fn().mockResolvedValue({
                    selectedProjectId: "default",
                }),
                set: vi.fn().mockResolvedValue(undefined),
            },
        };

        await setStoredProjectId(
            "project-python",
            storage,
        );

        expect(storage.local.set).toHaveBeenCalledWith({
            selectedProjectId: "project-python",
        });

        const projectId = await getStoredProjectId(
            storage,
        );

        expect(storage.local.get).toHaveBeenCalledWith(
            "selectedProjectId",
        );

        expect(projectId).toBe("default");
    });
});