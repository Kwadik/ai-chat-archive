import type { ChatContext } from "../chat/chat-context";
import {
    readMarkdownFromClipboard,
    type ClipboardReader,
} from "../clipboard/clipboard";
import { createExtensionRoot } from "./extension-root";
import {
    createExtensionPanel,
    showExtensionEditor,
    showHomeScreen,
    showProjectCreation,
    showProjectSelection,
} from "./extension-panel";
import type { ProjectCreationContext } from "./navigation-context";

export interface ExtensionUI {
    context: ChatContext;
    openEditor(initialMarkdown: string): void;
    openEditorFromClipboard(): Promise<void>;
    openHome(): Promise<void>;
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

    const showProjects = async (
        initialMarkdown: string,
        onSelect?: (projectId: string) => void | Promise<void>,
    ): Promise<void> => {
        const projects = await options.listProjects();

        showProjectSelection(
            panel,
            projects,
            async (projectId) => {
                await options.saveSelectedProjectId?.(projectId);
                options.selectedProjectId = projectId;

                if (onSelect) {
                    await onSelect(projectId);
                    return;
                }

                showExtensionEditor(
                    panel,
                    initialMarkdown,
                    (markdown) => onSave(markdown, context),
                    onCancel,
                );
            },
            () => {
                showProjectCreation(
                    panel,
                    "Мой проект",
                    async (name) => {
                        const project = await options.createProject(name);
                        await options.saveSelectedProjectId?.(project.id);
                        options.selectedProjectId = project.id;

                        if (onSelect) {
                            await onSelect(project.id);
                            return;
                        }

                        showExtensionEditor(
                            panel,
                            initialMarkdown,
                            (markdown) => onSave(markdown, context),
                            onCancel,
                        );
                    },
                    () => {
                        void showProjects(initialMarkdown, onSelect);
                    },
                    {
                        returnTo: "project-selection",
                        data: {
                            projectName: "Мой проект",
                        },
                    },
                );
            },
        );
    };

    return {
        context,

        async openHome(): Promise<void> {
            const projects = await options.listProjects();
            const selectedProject = projects.find(
                (project) => project.id === options.selectedProjectId,
            );

            showHomeScreen(panel, {
                currentProjectName: selectedProject?.name ?? null,
                onShowProjects: () => {
                    void showProjects("", () => this.openHome());
                },
                onCreateProject: () => {
                    showProjectCreation(
                        panel,
                        "Мой проект",
                        async (name) => {
                            const project = await options.createProject(name);
                            await options.saveSelectedProjectId?.(project.id);
                            options.selectedProjectId = project.id;
                            await this.openHome();
                        },
                        () => {
                            void this.openHome();
                        },
                        {
                            returnTo: "home",
                            data: {
                                projectName: "Мой проект",
                            },
                        },
                    );
                },
                onEditProject: () => {
                    // Редактирование проекта добавим отдельным шагом.
                },
                onSaveChatGPTMessage: () => {
                    // Подключим сохранение сообщения отдельным шагом.
                },
                onSaveUserMessage: () => {
                    // Подключим сохранение сообщения отдельным шагом.
                },
            });
        },

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
                            showProjectCreation(
                                panel,
                                "Мой проект",
                                async (name) => {
                                    const project = await options.createProject(name);
                                    await options.saveSelectedProjectId?.(project.id);
                                    options.selectedProjectId = project.id;
                                    this.openEditor(markdown ?? "");
                                },
                                () => {
                                    void options.listProjects().then((projects) => {
                                        showProjectSelection(
                                            panel,
                                            projects,
                                            async (projectId) => {
                                                await options.saveSelectedProjectId?.(projectId);
                                                options.selectedProjectId = projectId;
                                                this.openEditor(markdown ?? "");
                                            },
                                            () => {
                                                // Этот переход настроим следующим шагом.
                                            },
                                        );
                                    });
                                },
                                {
                                    returnTo: "project-selection",
                                    data: {
                                        projectName: "Мой проект",
                                    },
                                },
                            );
                        },
                    );
                    return;
                }

                showProjectCreation(
                    panel,
                    "Мой проект",
                    async (name) => {
                        const project = await options.createProject(name);
                        await options.saveSelectedProjectId?.(project.id);
                        options.selectedProjectId = project.id;

                        showExtensionEditor(
                            panel,
                            markdown ?? "",
                            (markdown) => onSave(markdown, context),
                            onCancel,
                        );
                    },
                    undefined,
                    {
                        returnTo: "home",
                        message: "Для сохранения сообщения необходимо выбрать или создать проект.",
                        data: {
                            projectName: "Мой проект",
                        },
                    },
                );
                return;
            }

            this.openEditor(markdown ?? "");
        },
    };
}