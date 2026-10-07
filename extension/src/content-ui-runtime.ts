import {
    getCurrentChatContext,
} from "./content";
import {
    createContentUI,
} from "./content-ui";
import type { ExtensionUI } from "./extension-ui";
import type { ProviderDocument } from "./providers/types";

export function initializeContentUI(
    document: Document,
    url: URL,
    onSave: (markdown: string) => void,
    onCancel: () => void,
): ExtensionUI | null {
    const context = getCurrentChatContext(
        url,
        {
            title: document.title,
        } satisfies ProviderDocument,
    );

    if (!context) {
        return null;
    }

    return createContentUI(
        document,
        context,
        onSave,
        onCancel,
    );
}