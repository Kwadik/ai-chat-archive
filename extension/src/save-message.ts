import type { ChatContext } from "./chat-context";
import type {
    CreatedMessage,
    ExtensionApiClient,
} from "./api-client";

export async function saveMessage(
    apiClient: ExtensionApiClient,
    context: ChatContext,
    markdown: string,
    projectId: string,
): Promise<CreatedMessage> {
    return apiClient.createMessage({
        projectId,
        provider: context.provider,
        chatId: context.chatId,
        role: "user",
        content: markdown,
    });
}