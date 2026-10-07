/**
 * @vitest-environment jsdom
 */
import {describe, expect, it} from "vitest";
import {createExtensionRoot} from "../src/extension-root";

describe("extension root", () => {
    it("creates an extension root element", () => {
        const root = createExtensionRoot(document);

        expect(root.tagName).toBe("DIV");
        expect(root.id).toBe("ai-chat-archive-root");
        expect(document.body.contains(root)).toBe(true);
    });

    it("does not create a duplicate root", () => {
        const first = createExtensionRoot(document);
        const second = createExtensionRoot(document);

        expect(second).toBe(first);
        expect(
            document.querySelectorAll("#ai-chat-archive-root"),
        ).toHaveLength(1);
    });

    it("attaches a shadow root", () => {
        const root = createExtensionRoot(document);

        expect(root.shadowRoot).not.toBeNull();
    });

    it("keeps the same shadow root", () => {
        const first = createExtensionRoot(document);
        const second = createExtensionRoot(document);

        expect(second.shadowRoot).toBe(first.shadowRoot);
    });

    it("keeps UI inside the shadow root", () => {
        const root = createExtensionRoot(document);

        const button = document.createElement("button");
        button.textContent = "Save";

        root.shadowRoot?.appendChild(button);

        expect(root.shadowRoot?.contains(button)).toBe(true);
        expect(document.body.contains(button)).toBe(false);
    });

    it("positions the root as a fixed overlay", () => {
        const root = createExtensionRoot(document);

        expect(root.style.position).toBe("fixed");
    });

    it("fills the viewport", () => {
        const root = createExtensionRoot(document);

        expect(root.style.inset).toBe("0px");
    });

    it("does not block page pointer events", () => {
        const root = createExtensionRoot(document);

        expect(root.style.pointerEvents).toBe("none");
    });

    it("allows shadow UI elements to receive pointer events", () => {
        const root = createExtensionRoot(document);

        const panel = document.createElement("div");
        panel.style.pointerEvents = "auto";

        root.shadowRoot?.appendChild(panel);

        expect(panel.style.pointerEvents).toBe("auto");
    });
});