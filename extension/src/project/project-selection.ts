import type { ExtensionStorage } from "../storage/extension-storage";
import { setSelectedProjectId } from "./project-config";

export async function selectProject(
    projectId: string,
    storage: ExtensionStorage,
): Promise<void> {
    await setSelectedProjectId(projectId, storage);
}