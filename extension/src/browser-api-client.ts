import { ExtensionApiClient } from "./api-client";

export const DEFAULT_API_BASE_URL =
    "http://127.0.0.1:8000";

export function createBrowserApiClient(
    baseUrl: string = DEFAULT_API_BASE_URL,
): ExtensionApiClient {
    return new ExtensionApiClient(baseUrl);
}