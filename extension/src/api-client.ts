export interface CreateMessageInput {
    projectId: string;
    provider: string;
    chatId: string;
    role: string;
    content: string;
}

export interface CreatedMessage {
    number: number;
    role: string;
    file_name: string;
}

type FetchLike = (
    input: RequestInfo | URL,
    init?: RequestInit,
) => Promise<Response>;

export class ExtensionApiClient {
    constructor(
        private readonly baseUrl: string,
        private readonly fetchFn: FetchLike = fetch,
    ) {}

    async createMessage(
        input: CreateMessageInput,
    ): Promise<CreatedMessage> {
        const url =
            `${this.baseUrl}/projects/${input.projectId}` +
            `/chats/${input.provider}/${input.chatId}/messages`;

        const response = await this.fetchFn(
            url,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    role: input.role,
                    content: input.content,
                }),
            },
        );

        if (!response.ok) {
            throw new Error(
                `API request failed with status ${response.status}`,
            );
        }

        return response.json();
    }
}