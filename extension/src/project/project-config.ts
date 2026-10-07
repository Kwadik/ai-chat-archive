import type { ExtensionStorage } from "../storage/extension-storage";
import {
    getStoredProjectId,
    setStoredProjectId,
} from "../storage/extension-storage";

export const DEFAULT_PROJECT_ID = "default";

export async function getSelectedProjectId(
    storage: ExtensionStorage,
): Promise<string> {
    const projectId = await getStoredProjectId(storage);

    return projectId ?? DEFAULT_PROJECT_ID;
}

export async function setSelectedProjectId(
    projectId: string,
    storage: ExtensionStorage,
): Promise<void> {
    await setStoredProjectId(
        projectId,
        storage,
    );
}