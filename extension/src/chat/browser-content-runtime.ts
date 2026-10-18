import { runContentScript } from "./content-runtime";
import type { ExtensionUIOptions } from "../ui/extension-ui";
import type { ChatContext } from "./chat-context";
import type { ClipboardReader } from "../clipboard/clipboard";
import type { ExtensionApiClient } from "../api/api-client";
import { saveMessage } from "../save/save-message";

export function runBrowserContentScript(
    onSave: (markdown: string, context: ChatContext) => void = () => {},
    onCancel: () => void = () => {},
    apiClient?: ExtensionApiClient,
    projectId: string | null = null,
    uiOptions?: ExtensionUIOptions
) {
    return runContentScript(
        {
            location: {
                href: window.location.href,
            },
        },
        document,
        (markdown, context) => {
            const selectedProjectId = uiOptions?.selectedProjectId ?? projectId;

            if (apiClient && selectedProjectId !== null) {
                void saveMessage(
                    apiClient,
                    context,
                    markdown,
                    selectedProjectId,
                );
            }

            onSave(markdown, context);
        },
        onCancel,
        navigator.clipboard ?? null,
        uiOptions
    );
}