// @vitest-environment jsdom

import { describe, expect, it } from "vitest";
import { createStylesheet } from "../../src/ui/create-stylesheet";

describe("createStylesheet", () => {
    it("creates a style element with the stylesheet marker", () => {
        const styles = createStylesheet(
            document,
            "[data-panel] { color: red; }",
        );

        expect(styles.tagName).toBe("STYLE");
        expect(styles.dataset.aiChatArchiveStyles).toBe("");
    });

    it("preserves the supplied CSS", () => {
        const css = "[data-panel] { box-sizing: border-box; }";

        const styles = createStylesheet(document, css);

        expect(styles.textContent).toBe(css);
    });
});