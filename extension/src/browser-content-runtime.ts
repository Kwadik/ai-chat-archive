import { runContentScript } from "./content-runtime";
import type { ChatContext } from "./chat-context";

export function runBrowserContentScript(
    onSave: (markdown: string, context: ChatContext) => void = () => {},
    onCancel: () => void = () => {},
) {
    return runContentScript(
        {
            location: {
                href: window.location.href,
            },
        },
        document,
        onSave,
        onCancel,
        navigator.clipboard ?? null,
    );
}