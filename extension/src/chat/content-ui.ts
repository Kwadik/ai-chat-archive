import {
    createExtensionUI,
    type ExtensionUI,
    type ExtensionUIOptions,
} from "../ui/extension-ui";
import type { ChatContext } from "./chat-context";
import type { ClipboardReader } from "../clipboard/clipboard";

export function createContentUI(
    document: Document,
    context: ChatContext,
    onSave: (markdown: string, context: ChatContext) => void,
    onCancel: () => void,
    clipboard: ClipboardReader | null,
    options?: ExtensionUIOptions,
): ExtensionUI {
    return createExtensionUI(
        document,
        context,
        onSave,
        onCancel,
        clipboard,
        options,
    );
}