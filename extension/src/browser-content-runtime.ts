import { runContentScript } from "./content-runtime";
import type { ChatContext } from "./chat-context";
import type { ClipboardReader } from "./clipboard";
import type { ExtensionApiClient } from "./api-client";
import { saveMessage } from "./save-message";

export function runBrowserContentScript(
    onSave: (markdown: string, context: ChatContext) => void = () => {},
    onCancel: () => void = () => {},
    apiClient?: ExtensionApiClient,
) {
    return runContentScript(
        {
            location: {
                href: window.location.href,
            },
        },
        document,
        (markdown, context) => {
            if (apiClient) {
                void saveMessage(
                    apiClient,
                    context,
                    markdown,
                    "default",
                );
            }

            onSave(markdown, context);
        },
        onCancel,
        navigator.clipboard ?? null,
    );
}