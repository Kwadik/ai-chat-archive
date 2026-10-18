import { initializeContentUI } from "./content-ui-runtime";
import type { ChatContext } from "./chat-context";
import type { ClipboardReader } from "../clipboard/clipboard";
import type { ExtensionUIOptions } from "../ui/extension-ui";

interface RuntimeContext {
    location: {
        href: string;
    };
}

export function runContentScript(
    runtime: RuntimeContext,
    document: Document,
    onSave: (markdown: string, context: ChatContext) => void,
    onCancel: () => void,
    clipboard: ClipboardReader | null,
    options?: ExtensionUIOptions
) {
    return initializeContentUI(
        document,
        new URL(runtime.location.href),
        onSave,
        onCancel,
        clipboard,
        options
    );
}