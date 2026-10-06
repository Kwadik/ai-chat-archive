import { describe, expect, it } from "vitest";
import type { ChatContext } from "../src/chat-context";

describe("ChatContext", () => {
    it("describes current chat context", () => {
        const context: ChatContext = {
            provider: "chatgpt",
            chatId: "abc123",
            title: "Python discussion",
        };

        expect(context.provider).toBe("chatgpt");
        expect(context.chatId).toBe("abc123");
        expect(context.title).toBe("Python discussion");
    });
});