import { runBrowserContentScript } from "./browser-content-runtime";
import { createBrowserApiClient } from "./browser-api-client";

const apiClient = createBrowserApiClient();

runBrowserContentScript(
    () => {},
    () => {},
    apiClient,
);