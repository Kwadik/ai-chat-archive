export interface ProviderDocument {
    title: string;
}

export interface ProviderAdapter {
    provider: string;

    canHandle(url: URL): boolean;

    getChatId(url: URL): string | null;

    getChatTitle(document: ProviderDocument): string | null;
}