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

    it("includes the compiled panel stylesheet in the content script", () => {
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

        const contentScript = readFileSync(
            contentScriptPath,
            "utf-8",
        );

        expect(contentScript).toContain(
            "[data-ai-chat-archive-panel]",
        );
        expect(contentScript).toContain(
            "box-sizing: border-box",
        );
        expect(contentScript).toContain("pointer-events: auto");
        expect(contentScript).toContain("position: absolute");
        expect(contentScript).toContain(
            "width: min(480px, 100vw - 32px)",
        );
        expect(contentScript).toContain("overflow-y: auto");
    });
});