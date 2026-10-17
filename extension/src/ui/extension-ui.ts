import type { ChatContext } from "../chat/chat-context";
import {
    readMarkdownFromClipboard,
    type ClipboardReader,
} from "../clipboard/clipboard";
import { createExtensionRoot } from "./extension-root";
import {
    createExtensionPanel,
    showExtensionEditor,
    showProjectCreation,
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
    options: {
        selectedProjectId: string | null;
        createProject: (name: string) => Promise<{ id: string; name: string }>;
    } = {
        selectedProjectId: "existing-project",
        createProject: async () => {
            throw new Error("Project creation is not configured");
        },
    },
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
            if (options.selectedProjectId === null) {
                showProjectCreation(panel);
                return;
            }

            const markdown = await readMarkdownFromClipboard(clipboard);
            this.openEditor(markdown ?? "");
        },
    };
}