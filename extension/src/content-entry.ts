import { getCurrentChatContext } from "./content";
import type { ProviderDocument } from "./providers/types";

export function initializeContentScript(
    url: URL,
    document: ProviderDocument,
): ReturnType<typeof getCurrentChatContext> {
    return getCurrentChatContext(url, document);
}