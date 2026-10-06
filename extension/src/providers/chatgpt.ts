import type { ProviderAdapter } from "./types";
import { getChatIdFromChatGPTUrl } from "./chatgpt-url";

export const chatgptProvider: ProviderAdapter = {
    provider: "chatgpt",

    canHandle(url: URL): boolean {
        return url.hostname === "chatgpt.com";
    },

    getChatId(url: URL): string | null {
        return getChatIdFromChatGPTUrl(url);
    },

    getChatTitle(document): string | null {
        const title = document.title.trim();

        return title || null;
    },
};