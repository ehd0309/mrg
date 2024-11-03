"use client";

import Chat from "@/app/chat/[id]/_inner/Chat";
import { Tabs, Tab, Card, CardBody } from "@nextui-org/react";

interface WrapperProps {
  id: string;
  version: "v1" | "v2" | "v3";
}

const Wrapper = ({ id, version }: WrapperProps) => {
  const cardClasses = "min-h-[calc(100vh-18rem)]";
  return (
    <div className="flex w-full flex-col">
      <Tabs color="primary" aria-label="Options">
        <Tab key="chat" title="CHAT">
          <Card className={`${cardClasses} border-none shadow-none`}>
            <CardBody className="flex flex-col justify-between relative">
              <Chat id={id} version={version} />
            </CardBody>
          </Card>
        </Tab>
        <Tab key="ocr" title="OCR">
          <Card className={cardClasses}>
            <CardBody>
              Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
              reprehenderit in voluptate velit esse cillum dolore eu fugiat
              nulla pariatur.
            </CardBody>
          </Card>
        </Tab>
        <Tab key="graph" title="GRAPH">
          <Card className={cardClasses}>
            <CardBody>
              Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
              officia deserunt mollit anim id est laborum.
            </CardBody>
          </Card>
        </Tab>
      </Tabs>
    </div>
  );
};

export default Wrapper;
