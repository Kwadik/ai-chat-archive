import { describe, expect, it } from "vitest";
import {
    readFileSync,
    existsSync,
} from "node:fs";
import { resolve } from "node:path";

describe("extension manifest", () => {
    it("configures the content script for ChatGPT", () => {
        const manifestPath = resolve(
            import.meta.dirname,
            "../manifest.json",
        );

        const manifest = JSON.parse(
            readFileSync(manifestPath, "utf-8"),
        );

        expect(manifest.manifest_version).toBe(3);
        expect(manifest.name).toBe("AI Chat Archive");
        expect(manifest.content_scripts).toEqual([
            {
                matches: ["https://chatgpt.com/*"],
                js: ["content-script.js"],
            },
        ]);
    });

    it("points to the built content script", () => {
        const manifestPath = resolve(
            import.meta.dirname,
            "../manifest.json",
        );

        const manifest = JSON.parse(
            readFileSync(manifestPath, "utf-8"),
        );

        expect(manifest.content_scripts?.[0]?.js).toEqual([
            "content-script.js",
        ]);
    });
});