export function createExtensionEditor(
    initialMarkdown: string,
    onSave: (markdown: string) => void,
    onCancel: () => void,
): HTMLDivElement {
    const editor = document.createElement("div");

    const textarea = document.createElement("textarea");
    textarea.dataset.aiChatArchiveEditor = "";
    textarea.value = initialMarkdown;

    const actions = document.createElement("div");

    const cancelButton = document.createElement("button");
    cancelButton.dataset.aiChatArchiveCancel = "";
    cancelButton.type = "button";
    cancelButton.textContent = "Cancel";

    cancelButton.addEventListener("click", () => {
        onCancel();
    });

    const saveButton = document.createElement("button");
    saveButton.dataset.aiChatArchiveSave = "";
    saveButton.type = "button";
    saveButton.textContent = "Save";

    saveButton.addEventListener("click", () => {
        onSave(textarea.value);
    });

    actions.appendChild(cancelButton);
    actions.appendChild(saveButton);

    editor.appendChild(textarea);
    editor.appendChild(actions);

    return editor;
}