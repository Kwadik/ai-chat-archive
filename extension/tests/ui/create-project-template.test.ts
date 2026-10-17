/**
 * @vitest-environment jsdom
 */
import { describe, expect, it } from "vitest";
import { createProjectForm } from "../../src/ui/create-project-template";

const templateHtml = `
    <form data-ai-chat-archive-create-project>
        <label>
            Название проекта
            <input
                type="text"
                data-ai-chat-archive-project-name
                required
            />
        </label>
        <button type="submit">Создать проект</button>
    </form>
`;

describe("createProjectForm", () => {
    it("creates the form and sets the initial project name", () => {
        const form = createProjectForm(
            document,
            templateHtml,
        );

        const nameInput = form.querySelector(
            "[data-ai-chat-archive-project-name]",
        ) as HTMLInputElement;

        expect(form.dataset.aiChatArchiveCreateProject).toBe("");
        expect(nameInput.value).toBe("Мой проект");
        expect(nameInput.required).toBe(true);
    });

    it("uses a provided initial project name", () => {
        const form = createProjectForm(
            document,
            templateHtml,
            "Рабочий проект",
        );

        const nameInput = form.querySelector(
            "[data-ai-chat-archive-project-name]",
        ) as HTMLInputElement;

        expect(nameInput.value).toBe("Рабочий проект");
    });

    it("throws when the form is missing from the template", () => {
        expect(() =>
            createProjectForm(document, "<div>Нет формы</div>"),
        ).toThrow("Project creation form template not found");
    });
});