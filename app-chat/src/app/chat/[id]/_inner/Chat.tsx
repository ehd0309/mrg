"use client";

import { ChatMessage } from "@/type/chat";
import { Button, Textarea } from "@nextui-org/react";
import Image from "next/image";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatProps {
  id: string;
  version: "v1" | "v2" | "v3";
  chatHistory: ChatMessage[];
  currentQuery: string;
  currentChat: string;
  isGenerating: boolean;
  setCurrentQuery: (query: string) => void;
  handleSendChat: () => void;
}

const Chat = ({
  chatHistory,
  currentQuery,
  currentChat,
  isGenerating,
  setCurrentQuery,
  handleSendChat,
}: ChatProps) => {
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