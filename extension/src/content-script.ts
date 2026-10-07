import { runBrowserContentScript } from "./chat/browser-content-runtime";
import { createBrowserApiClient } from "./api/browser-api-client";
import { initializeBrowserContentScript } from "./chat/browser-content-script";

void initializeBrowserContentScript(
    chrome,
    createBrowserApiClient(),
    runBrowserContentScript,
);