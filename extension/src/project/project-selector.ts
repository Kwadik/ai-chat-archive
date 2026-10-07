export interface ProjectOption {
    id: string;
    name: string;
}

export function createProjectSelector(
    projects: ProjectOption[],
    selectedProjectId: string,
    onSelect: (projectId: string) => void,
): HTMLDivElement {
    const container = document.createElement("div");

    const select = document.createElement("select");
    select.dataset.aiChatArchiveProject = "";

    for (const project of projects) {
        const option = document.createElement("option");

        option.value = project.id;
        option.textContent = project.name;
        option.selected = project.id === selectedProjectId;

        select.appendChild(option);
    }

    select.addEventListener("change", () => {
        onSelect(select.value);
    });

    container.appendChild(select);

    return container;
}