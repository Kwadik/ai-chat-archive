/**
 * @vitest-environment jsdom
 */
import { describe, expect, it, vi } from "vitest";
import { createProjectSelector } from "../../src/project/project-selector";

describe("createProjectSelector", () => {
    it("shows projects and saves the selected project", async () => {
        const projects = [
            { id: "default", name: "Default" },
            { id: "python", name: "Python" },
        ];

        const onSelect = vi.fn();

        const selector = createProjectSelector(
            projects,
            "default",
            onSelect,
        );

        document.body.appendChild(selector);

        const select = selector.querySelector(
            "[data-ai-chat-archive-project]",
        );

        expect(select).toBeInstanceOf(HTMLSelectElement);

        const options = Array.from(
            (select as HTMLSelectElement).options,
        );

        expect(options.map((option) => ({
            value: option.value,
            text: option.textContent,
        }))).toEqual([
            { value: "default", text: "Default" },
            { value: "python", text: "Python" },
        ]);

        expect(
            (select as HTMLSelectElement).value,
        ).toBe("default");

        (select as HTMLSelectElement).value = "python";
        select?.dispatchEvent(
            new Event("change", { bubbles: true }),
        );

        expect(onSelect).toHaveBeenCalledWith("python");
    });
});