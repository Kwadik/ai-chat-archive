import { runBrowserContentScript } from "./browser-content-runtime";
import { createBrowserApiClient } from "./browser-api-client";
import { initializeBrowserContentScript } from "./browser-content-script";

void initializeBrowserContentScript(
    chrome,
    createBrowserApiClient(),
    runBrowserContentScript,
);