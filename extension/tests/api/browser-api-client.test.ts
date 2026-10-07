import { describe, expect, it } from "vitest";
import {
    createBrowserApiClient,
    DEFAULT_API_BASE_URL,
} from "../../src/api/browser-api-client";
import { ExtensionApiClient } from "../../src/api/api-client";

describe("createBrowserApiClient", () => {
    it("creates an API client for the configured base URL", () => {
        const client = createBrowserApiClient(
            "http://127.0.0.1:8000",
        );

        expect(client).toBeInstanceOf(ExtensionApiClient);
    });

    it("uses the local API as the default base URL", () => {
        const client = createBrowserApiClient();

        expect(client).toBeInstanceOf(ExtensionApiClient);
        expect(DEFAULT_API_BASE_URL).toBe(
            "http://127.0.0.1:8000",
        );
    });
});