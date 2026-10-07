export interface ExtensionStorage {
    local: {
        get(
            key: string,
        ): Promise<Record<string, unknown>>;

        set(
            values: Record<string, unknown>,
        ): Promise<void>;
    };
}

const SELECTED_PROJECT_KEY = "selectedProjectId";

export async function setStoredProjectId(
    projectId: string,
    storage: ExtensionStorage,
): Promise<void> {
    await storage.local.set({
        [SELECTED_PROJECT_KEY]: projectId,
    });
}

export async function getStoredProjectId(
    storage: ExtensionStorage,
): Promise<string | null> {
    const values = await storage.local.get(
        SELECTED_PROJECT_KEY,
    );

    const projectId = values[SELECTED_PROJECT_KEY];

    return typeof projectId === "string"
        ? projectId
        : null;
}