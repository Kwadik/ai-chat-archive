export function createExtensionRoot(
    document: Document,
): HTMLDivElement {
    const existingRoot = document.getElementById(
        "ai-chat-archive-root",
    );

    if (existingRoot instanceof HTMLDivElement) {
        return existingRoot;
    }

    const root = document.createElement("div");

    root.id = "ai-chat-archive-root";
    root.style.position = "fixed";
    root.style.inset = "0";
    root.style.pointerEvents = "none";
    root.attachShadow({mode: "open"});

    document.body.appendChild(root);

    return root;
}