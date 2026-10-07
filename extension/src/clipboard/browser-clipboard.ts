import {
    readMarkdownFromClipboard,
    type ClipboardReader,
} from "./clipboard";

export async function readBrowserClipboard(
    clipboard: ClipboardReader | null,
): Promise<string | null> {
    return readMarkdownFromClipboard(clipboard);
}