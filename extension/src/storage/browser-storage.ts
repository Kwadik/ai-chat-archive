import type { ExtensionStorage } from "./extension-storage";

export interface BrowserChrome {
    storage: ExtensionStorage;
}

export function getBrowserStorage(
    chrome: BrowserChrome,
): ExtensionStorage {
    return chrome.storage;
}