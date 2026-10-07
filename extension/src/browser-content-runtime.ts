import { runContentScript } from "./content-runtime";

export function runBrowserContentScript() {
    return runContentScript(
        {
            location: {
                href: window.location.href,
            },
        },
        document,
        () => {},
        () => {},
    );
}