import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

describe("extension build configuration", () => {
    it("defines a build script", () => {
        const packagePath = resolve(
            import.meta.dirname,
            "../package.json",
        );

        const packageJson = JSON.parse(
            readFileSync(packagePath, "utf-8"),
        );

        expect(packageJson.scripts?.build).toBeDefined();
    });
});