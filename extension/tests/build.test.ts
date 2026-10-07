import { describe, expect, it } from "vitest";
import {
    existsSync,
    readFileSync,
} from "node:fs";
import { resolve } from "node:path";
import { execSync } from "node:child_process";

describe("extension build", () => {
    it("produces the content script", () => {
        const extensionRoot = resolve(
            import.meta.dirname,
            "..",
        );

        execSync("npm run build", {
            cwd: extensionRoot,
            stdio: "pipe",
            shell: process.platform === "win32" ? "cmd.exe" : "/bin/sh",
        });

        const contentScriptPath = resolve(
            extensionRoot,
            "dist/content-script.js",
        );

        expect(existsSync(contentScriptPath)).toBe(true);
    });

    it("produces a standalone content script", () => {
        const extensionRoot = resolve(
            import.meta.dirname,
            "..",
        );

        const contentScriptPath = resolve(
            extensionRoot,
            "dist/content-script.js",
        );

        const contentScript = readFileSync(
            contentScriptPath,
            "utf-8",
        );

        expect(contentScript).not.toMatch(/\bimport\s+/);
        expect(contentScript).not.toMatch(/\bexport\s+/);
    });
});