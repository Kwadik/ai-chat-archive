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
    showProjectSelection,
} from "./extension-panel";

export interface ExtensionUI {
    context: ChatContext;
    openEditor(initialMarkdown: string): void;
    openEditorFromClipboard(): Promise<void>;
}

export interface ExtensionUIOptions {
    selectedProjectId: string | null;
    createProject: (name: string) => Promise<{ id: string; name: string }>;
    listProjects: () => Promise<{ id: string; name: string }[]>;
    saveSelectedProjectId?: (projectId: string) => Promise<void>;
}

export function createExtensionUI(
    document: Document,
    context: ChatContext,
    onSave: (markdown: string, context: ChatContext) => void,
    onCancel: () => void,
    clipboard: ClipboardReader | null,
    options: ExtensionUIOptions = {
        selectedProjectId: "existing-project",
        createProject: async () => {
            throw new Error("Project creation is not configured");
        },
        listProjects: async () => [],
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
            const markdown = await readMarkdownFromClipboard(clipboard);
            const projects = options.selectedProjectId === null
                ? await options.listProjects()
                : [];

            if (options.selectedProjectId === null) {
                if (projects.length > 0) {
                    showProjectSelection(
                        panel,
                        projects,
                        async (projectId) => {
                            await options.saveSelectedProjectId?.(projectId);
                            options.selectedProjectId = projectId;
                            this.openEditor(markdown ?? "");
                        },
                        () => {
                            showProjectCreation(panel, "Мой проект", async (name) => {
                                const project = await options.createProject(name);
                                await options.saveSelectedProjectId?.(project.id);
                                options.selectedProjectId = project.id;

                                showExtensionEditor(
                                    panel,
                                    markdown ?? "",
                                    (markdown) => onSave(markdown, context),
                                    onCancel,
                                );
                            });
                        },
                    );
                    return;
                }

                showProjectCreation(panel, "Мой проект", async (name) => {
                    const project = await options.createProject(name);
                    await options.saveSelectedProjectId?.(project.id);
                    options.selectedProjectId = project.id;

                    showExtensionEditor(
                        panel,
                        markdown ?? "",
                        (markdown) => onSave(markdown, context),
                        onCancel,
                    );
                });
                return;
            }

            this.openEditor(markdown ?? "");
        },
    };
}