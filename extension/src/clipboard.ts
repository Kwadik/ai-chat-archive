export interface ClipboardReader {
    readText(): Promise<string>;
}

export async function readMarkdownFromClipboard(
    clipboard: ClipboardReader | null,
): Promise<string | null> {
    if (clipboard === null) {
        return null;
    }

    try {
        return await clipboard.readText();
    } catch {
        return null;
    }
}