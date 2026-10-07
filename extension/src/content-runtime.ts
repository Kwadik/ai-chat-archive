import { initializeContentUI } from "./content-ui-runtime";

interface RuntimeContext {
    location: {
        href: string;
    };
}

export function runContentScript(
    runtime: RuntimeContext,
    document: Document,
    onSave: (markdown: string) => void,
    onCancel: () => void,
) {
    return initializeContentUI(
        document,
        new URL(runtime.location.href),
        onSave,
        onCancel,
    );
}