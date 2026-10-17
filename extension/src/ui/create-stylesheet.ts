export function createStylesheet(
    document: Document,
    cssText: string,
): HTMLStyleElement {
    const styles = document.createElement("style");

    styles.dataset.aiChatArchiveStyles = "";
    styles.textContent = cssText;

    return styles;
}