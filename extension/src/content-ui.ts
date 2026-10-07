import {
    createExtensionUI,
    type ExtensionUI,
} from "./extension-ui";
import type { ChatContext } from "./chat-context";
import type { ClipboardReader } from "./clipboard";

export function createContentUI(
    document: Document,
    context: ChatContext,
    onSave: (markdown: string, context: ChatContext) => void,
    onCancel: () => void,
    clipboard: ClipboardReader | null,
): ExtensionUI {
    return createExtensionUI(
        document,
        context,
        onSave,
        onCancel,
        clipboard,
    );
}