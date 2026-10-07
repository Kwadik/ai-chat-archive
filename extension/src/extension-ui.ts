import type { ChatContext } from "./chat-context";
import { createExtensionRoot } from "./extension-root";
import {
    createExtensionPanel,
    showExtensionEditor,
} from "./extension-panel";

export interface ExtensionUI {
    context: ChatContext;
    openEditor(initialMarkdown: string): void;
}

export function createExtensionUI(
    document: Document,
    context: ChatContext,
    onSave: (markdown: string) => void,
    onCancel: () => void,
): ExtensionUI {
    const root = createExtensionRoot(document);
    const panel = createExtensionPanel(root);

    return {
        context,

        openEditor(initialMarkdown: string): void {
            showExtensionEditor(
                panel,
                initialMarkdown,
                onSave,
                onCancel,
            );
        },
    };
}