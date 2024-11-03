"use client";

import { api } from "@/api";
import { ChatMessage } from "@/type/chat";
import { Button, Input, Textarea } from "@nextui-org/react";
import Image from "next/image";
import { useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatProps {
  id: string;
  version: "v1" | "v2" | "v3";
}

const Chat = ({ id, version }: ChatProps) => {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([
    {
      message: `### 안녕하세요 \n\n 무엇을 도와드릴까요`,
      sender: "bot",
      timestamp: new Date().toString(),
    },
  ]);
  const [currentQuery, setCurrentQuery] = useState<string>("");
  const [currentChat, setCurrentChat] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const handleSendChat = async () => {
    setCurrentQuery("");
    setChatHistory((prev) => [
      ...prev,
      {
        message: currentQuery,
        sender: "user",
        timestamp: new Date().toString(),
      },
    ]);
    const { decoder, reader } = await api.postRagChat(
      id,
      currentQuery,
      version
    );
    setIsGenerating(true);
    let finalMessage = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      let message = chunk;
      finalMessage += message;
      setCurrentChat((prevMessages) => prevMessages + message);
    }
    setIsGenerating(false);
    setCurrentChat(() => "");
    setChatHistory((prev) => [
      ...prev,
      {
        message: finalMessage,
        sender: "bot",
        timestamp: new Date().toString(),
      },
    ]);
  };
  return (
    <>
      <div className="flex flex-col gap-4">
        {chatHistory.map((chat) => (
          <ChatBox key={chat.timestamp} {...chat} />
        ))}
        {currentChat !== "" && (
          <ChatBox message={currentChat} sender="bot" timestamp="" />
        )}
        <br />
        <br />
        <br />
        <br />
      </div>
      <div className="md:w-[700px] lg:w-[1000px] bg-primary-100 relative">
        <div
          className="fixed max-w-[calc(100%-280px)]"
          style={{ bottom: 36, width: "inherit" }}
        >
          <Textarea
            isDisabled={isGenerating}
            disabled={isGenerating}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                handleSendChat();
                e.preventDefault();
              }
            }}
            type="text"
            value={currentQuery}
            onValueChange={setCurrentQuery}
            className="w-full border border-default-400 rounded-md"
            placeholder="채팅 입력..."
            endContent={
              <Button
                onClick={handleSendChat}
                isIconOnly
                size="sm"
                color="secondary"
                radius="lg"
                className="bg-black rounded-full"
              >
                <Image
                  alt="chat"
                  src="/images/chat.svg"
                  width={24}
                  height={24}
                  color="white"
                  style={{ fill: "white" }}
                />
              </Button>
            }
          />
        </div>
      </div>
    </>
  );
};

const ChatBox = ({ message, sender, timestamp }: ChatMessage) => {
  return (
    <div
      className={`flex gap-4 items-start ${
        sender === "user" ? "flex-row-reverse" : "flex-row"
      }`}
    >
      <div
        className={`rounded-full bg-default-100 p-2 w-fit translate-y-1 ${
          sender === "user" ? "bg-primary-100" : "bg-secondary-100"
        }`}
      >
        <Image
          alt="chat-user"
          width={24}
          height={24}
          src={`/images/${sender === "user" ? "user.svg" : "ai.svg"}`}
        />
      </div>
      <div
        className="rounded-md bg-default-100 min-w-[300px] pt-2 px-4 pb-4"
        style={{ maxWidth: "calc(100% - 60px)" }}
      >
        <Markdown className="markdown-wrapper" remarkPlugins={[remarkGfm]}>
          {message}
        </Markdown>
        {timestamp ? (
          <p className="text-xs text-default-400">{timestamp}</p>
        ) : (
          <p>&nbsp;</p>
        )}
      </div>
    </div>
  );
};

export default Chat;
