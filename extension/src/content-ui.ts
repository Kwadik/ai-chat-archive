import {
    createExtensionUI,
    type ExtensionUI,
} from "./extension-ui";
import type { ChatContext } from "./chat-context";

export function createContentUI(
    document: Document,
    context: ChatContext,
    onSave: (markdown: string) => void,
    onCancel: () => void,
): ExtensionUI {
    return createExtensionUI(
        document,
        context,
        onSave,
        onCancel,
    );
}