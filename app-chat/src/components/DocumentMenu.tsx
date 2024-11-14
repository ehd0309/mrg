"use client";

import { useDocumentList } from "@/hooks/useDocuments";
import { Accordion, AccordionItem } from "@nextui-org/react";
import Link from "next/link";

const DocumentMenu = () => {
  const { documents } = useDocumentList();
  return (
    <Accordion className="px-0">
      <AccordionItem
        key="documents"
        aria-label="documents-a"
        title="Documents"
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
            href={`/document/${document.id}`}
            className="text-sm block px-8 py-2 hover:bg-black block text-default-300"
          >
            <p className="hover:text-default-100">{document.documentName}</p>
            <div className="flex items-center justify-between text-default-500 text-[10px] gap-2">
              <p>{document?.description}</p>
              <p>{new Date(document?.createdAt ?? "").toDateString()}</p>
            </div>
          </Link>
        ))}
      </AccordionItem>
    </Accordion>
  );
};

export default DocumentMenu;
