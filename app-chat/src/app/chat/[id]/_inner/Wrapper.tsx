"use client";

import { useEffect, useState } from "react";
import Chat from "@/app/chat/[id]/_inner/Chat";
import { Tabs, Tab, Card, CardBody } from "@nextui-org/react";
import { ChatMessage } from "@/type/chat";
import { api } from "@/api";
import Pipeline from "./Pipeline";
import PageTitle from "@/components/PageTitle";
import { useRag } from "@/hooks/useRag";

interface WrapperProps {
  id: string;
}

const Wrapper = ({ id }: WrapperProps) => {
  const { document } = useRag(id);
  const cardClasses = "min-h-[calc(100vh-18rem)]";

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
  const [preImage, setPreImage] = useState(null);
  const [postImage, setPostImage] = useState(null);

  useEffect(() => {
    (async () => {
      const { post_process_image, pre_process_image } =
        await api.getRagPipelineById(document.idxName, document.version);
      setPostImage(post_process_image);
      setPreImage(pre_process_image);
    })();
  }, [id]);

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
      document.idxName,
      currentQuery,
      document.version
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
      <PageTitle title={"TITLE"} />
      <div className="flex w-full flex-col">
        <Tabs color="primary" aria-label="Options">
          <Tab key="chat" title="CHAT">
            <Card className={`${cardClasses} border-none shadow-none`}>
              <CardBody className="flex flex-col justify-between relative">
                <Chat
                  id={id}
                  version={document.version}
                  chatHistory={chatHistory}
                  currentQuery={currentQuery}
                  currentChat={currentChat}
                  isGenerating={isGenerating}
                  setCurrentQuery={setCurrentQuery}
                  handleSendChat={handleSendChat}
                />
              </CardBody>
            </Card>
          </Tab>
          <Tab key="ocr" title="OCR">
            <Card className={cardClasses}>
              <CardBody>
                Ut enim ad minim veniam, quis nostrud exercitation ullamco
                laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure
                dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla pariatur.
              </CardBody>
            </Card>
          </Tab>
          <Tab key="graph" title="GRAPH">
            <Card className={`${cardClasses} border-none shadow-none`}>
              <CardBody>
                <Pipeline
                  pre_process_image={preImage}
                  post_process_image={postImage}
                />
              </CardBody>
            </Card>
          </Tab>
        </Tabs>
      </div>
    </>
  );
};

export default Wrapper;
