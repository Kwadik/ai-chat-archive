import {
    getCurrentChatContext,
} from "./content";
import {
    createContentUI,
} from "./content-ui";
import type { ExtensionUI } from "./extension-ui";
import type { ProviderDocument } from "./providers/types";
import type { ChatContext } from "./chat-context";
import type { ClipboardReader } from "./clipboard";

export function initializeContentUI(
    document: Document,
    url: URL,
    onSave: (markdown: string, context: ChatContext) => void,
    onCancel: () => void,
    clipboard: ClipboardReader | null,
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
        clipboard,
    );
}