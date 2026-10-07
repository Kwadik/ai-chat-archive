import { describe, expect, it, vi } from "vitest";
import type { ChatContext } from "../src/chat-context";
import type { ExtensionApiClient } from "../src/api-client";
import { saveMessage } from "../src/save-message";

describe("saveMessage", () => {
    it("creates a message using the chat context", async () => {
        const apiClient = {
            createMessage: vi.fn().mockResolvedValue({
                number: 1,
                role: "user",
                file_name: "001-user.md",
            }),
        } as unknown as ExtensionApiClient;

        const context: ChatContext = {
            provider: "chatgpt",
            chatId: "chat-123",
            title: "Test chat",
        };

        const result = await saveMessage(
            apiClient,
            context,
            "Cleaned **Markdown**",
            "default",
        );

        expect(apiClient.createMessage).toHaveBeenCalledWith({
            projectId: "default",
            provider: "chatgpt",
            chatId: "chat-123",
            role: "user",
            content: "Cleaned **Markdown**",
        });

        expect(result).toEqual({
            number: 1,
            role: "user",
            file_name: "001-user.md",
        });
    });

    it("creates a message in the selected project", async () => {
        const apiClient = {
            createMessage: vi.fn().mockResolvedValue({
                number: 1,
                role: "user",
                file_name: "001-user.md",
            }),
        } as unknown as ExtensionApiClient;

        const context: ChatContext = {
            provider: "chatgpt",
            chatId: "chat-123",
            title: "Test chat",
        };

        await saveMessage(
            apiClient,
            context,
            "Cleaned Markdown",
            "project-python",
        );

        expect(apiClient.createMessage).toHaveBeenCalledWith({
            projectId: "project-python",
            provider: "chatgpt",
            chatId: "chat-123",
            role: "user",
            content: "Cleaned Markdown",
        });
    });
});