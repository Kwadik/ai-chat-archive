import { initializeContentScript } from "./content-entry";

interface RuntimeContext {
    location: {
        href: string;
    };
    document: {
        title: string;
    };
}

export function runContentScript(runtime: RuntimeContext) {
    return initializeContentScript(
        new URL(runtime.location.href),
        runtime.document,
    );
}