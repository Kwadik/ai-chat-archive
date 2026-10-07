import { describe, expect, it } from "vitest";
import {
    getBrowserStorage,
} from "../../src/storage/browser-storage";

describe("getBrowserStorage", () => {
    it("returns chrome local storage", () => {
        const storage = {
            local: {
                get: async () => ({}),
                set: async () => {},
            },
        };

        const chrome = {
            storage,
        };

        expect(
            getBrowserStorage(chrome),
        ).toBe(storage);
    });

    it("exposes local get and set through the storage contract", async () => {
        const storage = {
            local: {
                get: async (key: string) => ({
                    [key]: "project-python",
                }),
                set: async () => {},
            },
        };

        const chrome = {
            storage,
        };

        const result = getBrowserStorage(chrome);

        expect(
            await result.local.get("selectedProjectId"),
        ).toEqual({
            selectedProjectId: "project-python",
        });

        await expect(
            result.local.set({
                selectedProjectId: "project-python",
            }),
        ).resolves.toBeUndefined();
    });
});