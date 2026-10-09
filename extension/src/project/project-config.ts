import type { ExtensionStorage } from "../storage/extension-storage";
import {
    getStoredProjectId,
    setStoredProjectId,
} from "../storage/extension-storage";

export async function getSelectedProjectId(
    storage: ExtensionStorage,
): Promise<string | null> {
    const projectId = await getStoredProjectId(storage);

    return projectId ?? null;
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