export function createProjectForm(
    document: Document,
    templateHtml: string,
    initialName = "Мой проект",
): HTMLFormElement {
    const template = document.createElement("template");
    template.innerHTML = templateHtml.trim();

    const form = template.content.querySelector(
        "[data-ai-chat-archive-create-project]",
    );

    if (!(form instanceof HTMLFormElement)) {
        throw new Error("Project creation form template not found");
    }

    const nameInput = form.querySelector(
        "[data-ai-chat-archive-project-name]",
    );

    if (!(nameInput instanceof HTMLInputElement)) {
        throw new Error("Project name input not found");
    }

    nameInput.value = initialName;

    return form;
}