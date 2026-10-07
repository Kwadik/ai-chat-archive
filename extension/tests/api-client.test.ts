import { describe, expect, it, vi } from "vitest";
import { ExtensionApiClient } from "../src/api-client";

describe("ExtensionApiClient", () => {
    it("creates a message through the local API", async () => {
        const fetchMock = vi.fn().mockResolvedValue(
            new Response(
                JSON.stringify({
                    number: 1,
                    role: "assistant",
                    file_name: "001-assistant.md",
                }),
                {
                    status: 201,
                    headers: {
                        "Content-Type": "application/json",
                    },
                },
            ),
        );

        const client = new ExtensionApiClient(
            "http://127.0.0.1:8765",
            fetchMock,
        );

        const result = await client.createMessage({
            projectId: "project-1",
            provider: "chatgpt",
            chatId: "chat-1",
            role: "assistant",
            content: "Привет!",
        });

        expect(fetchMock).toHaveBeenCalledWith(
            "http://127.0.0.1:8765/projects/project-1/chats/chatgpt/chat-1/messages",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    role: "assistant",
                    content: "Привет!",
                }),
            },
        );

        expect(result).toEqual({
            number: 1,
            role: "assistant",
            file_name: "001-assistant.md",
        });
    });

    it("throws when the API returns an error", async () => {
        const fetchMock = vi.fn().mockResolvedValue(
            new Response(
                JSON.stringify({
                    error: "Chat not found",
                }),
                {
                    status: 404,
                    headers: {
                        "Content-Type": "application/json",
                    },
                },
            ),
        );

        const client = new ExtensionApiClient(
            "http://127.0.0.1:8765",
            fetchMock,
        );

        await expect(
            client.createMessage({
                projectId: "project-1",
                provider: "chatgpt",
                chatId: "missing-chat",
                role: "assistant",
                content: "Привет!",
            }),
        ).rejects.toThrow();
    });
});