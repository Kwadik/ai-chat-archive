import type { ChatContext } from "./chat-context";
import {
    readMarkdownFromClipboard,
    type ClipboardReader,
} from "./clipboard";
import { createExtensionRoot } from "./extension-root";
import {
    createExtensionPanel,
    showExtensionEditor,
} from "./extension-panel";

export interface ExtensionUI {
    context: ChatContext;
    openEditor(initialMarkdown: string): void;
    openEditorFromClipboard(): Promise<void>;
}

export function createExtensionUI(
    document: Document,
    context: ChatContext,
    onSave: (markdown: string, context: ChatContext) => void,
    onCancel: () => void,
    clipboard: ClipboardReader | null,
): ExtensionUI {
    const root = createExtensionRoot(document);
    const panel = createExtensionPanel(root);

    return {
        context,

        openEditor(initialMarkdown: string): void {
            showExtensionEditor(
                panel,
                initialMarkdown,
                (markdown) => {
                    onSave(markdown, context);
                },
                onCancel,
            );
        },

        async openEditorFromClipboard(): Promise<void> {
            const markdown = await readMarkdownFromClipboard(
                clipboard,
            );

            this.openEditor(markdown ?? "");
        },
    };
}