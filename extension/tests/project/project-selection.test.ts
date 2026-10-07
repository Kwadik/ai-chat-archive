import { describe, expect, it, vi } from "vitest";
import {
    selectProject,
} from "../../src/project/project-selection";
import type { ExtensionStorage } from "../../src/storage/extension-storage";

describe("selectProject", () => {
    it("saves the selected project", async () => {
        const storage: ExtensionStorage = {
            local: {
                get: vi.fn(),
                set: vi.fn().mockResolvedValue(undefined),
            },
        };

        await selectProject("python", storage);

        expect(storage.local.set).toHaveBeenCalledWith({
            selectedProjectId: "python",
        });
    });
});