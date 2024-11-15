"use client";

import { useRagList } from "@/hooks/useRag";
import { Accordion, AccordionItem } from "@nextui-org/react";
import Link from "next/link";

const RAGMenu = () => {
  const { documents } = useRagList();
  return (
    <Accordion className="px-0">
      <AccordionItem
        key="rags"
        aria-label="rags-a"
        title="RAG-Q&A"
        classNames={{
          title: "px-8",
          subtitle: "px-8",
          trigger: "py-1",
          indicator: "px-8",
        }}
      >
        {documents?.map((document) => (
          <Link
            key={document.id}
            href={`/chat/${document.id}`}
            className="text-sm block px-8 py-2 hover:bg-black block text-default-300"
          >
            <p className="hover:text-default-100">{document?.name}</p>
            <div className="flex items-center justify-between text-default-500 text-[10px] gap-2">
              {document?.description && <p>{document?.description}</p>}
              <p>
                {new Date((document as any)?.createdAt ?? "").toDateString()}
              </p>
            </div>
          </Link>
        ))}
      </AccordionItem>
    </Accordion>
  );
};

export default RAGMenu;
