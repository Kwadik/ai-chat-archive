import { getBrowserStorage } from "./browser-storage";
import { getSelectedProjectId } from "./project-config";
import {
    runBrowserContentScript,
} from "./browser-content-runtime";
import type { ExtensionApiClient } from "./api-client";

export async function initializeBrowserContentScript(
    chrome: {
        storage: {
            local: {
                get(
                    key: string,
                ): Promise<Record<string, unknown>>;

                set(
                    values: Record<string, unknown>,
                ): Promise<void>;
            };
        };
    },
    apiClient: ExtensionApiClient,
    run: typeof runBrowserContentScript = runBrowserContentScript,
): Promise<void> {
    const storage = getBrowserStorage(chrome);
    const projectId = await getSelectedProjectId(storage);

    run(
        () => {},
        () => {},
        apiClient,
        projectId,
    );
}