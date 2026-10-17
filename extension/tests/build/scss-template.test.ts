// @vitest-environment node

import { describe, expect, it } from "vitest";
import { compile } from "sass";
import { readFile } from "node:fs/promises";
import * as path from "node:path";

describe("SCSS template", () => {
    it("compiles the panel stylesheet", async () => {
        const filePath = path.resolve(
            process.cwd(),
            "src/ui/styles/extension-panel.scss",
        );

        const source = await readFile(filePath, "utf8");
        const result = compile(filePath);

        expect(source).toContain("[data-ai-chat-archive-panel]");
        expect(result.css).toContain("[data-ai-chat-archive-panel]");
        expect(result.css).toContain("box-sizing: border-box");
    });
});