export function getChatIdFromChatGPTUrl(url: URL): string | null {
    const match = url.pathname.match(/^\/c\/([^/]+)$/);

    return match ? match[1] : null;
}