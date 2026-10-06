import { chatgptProvider } from "./providers/chatgpt";
import type { ProviderDocument } from "./providers/types";
import type { ChatContext } from "./chat-context";

export function getCurrentProvider(url: URL) {
    if (chatgptProvider.canHandle(url)) {
        return chatgptProvider;
    }

    return null;
}

export function getCurrentChatId(url: URL): string | null {
    const provider = getCurrentProvider(url);

    if (!provider) {
        return null;
    }

    return provider.getChatId(url);
}

export function getCurrentChatTitle(
    url: URL,
    document: ProviderDocument,
): string | null {
    const provider = getCurrentProvider(url);

    if (!provider) {
        return null;
    }

    return provider.getChatTitle(document);
}

export function getCurrentChatContext(
    url: URL,
    document: ProviderDocument,
): ChatContext | null {
    const provider = getCurrentProvider(url);

    if (!provider) {
        return null;
    }

    const chatId = provider.getChatId(url);

    if (!chatId) {
        return null;
    }

    return {
        provider: provider.provider,
        chatId,
        title: provider.getChatTitle(document),
    };
}

export function getCurrentChatUrl(
    url: URL,
): string | null {
    const provider = getCurrentProvider(url);

    if (!provider) {
        return null;
    }

    const chatId = provider.getChatId(url);

    if (!chatId) {
        return null;
    }

    return provider.getChatUrl(chatId);
}