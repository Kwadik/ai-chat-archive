export type ScreenId =
    | "home"
    | "project-selection"
    | "project-creation"
    | "editor";

export interface NavigationContext<TData = unknown> {
    returnTo: ScreenId;
    message?: string;
    data?: TData;
}

export interface ProjectCreationData {
    projectName?: string;
}

export type ProjectCreationContext =
    NavigationContext<ProjectCreationData>;