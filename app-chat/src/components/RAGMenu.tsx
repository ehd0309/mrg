"use client";

import { Accordion, AccordionItem } from "@nextui-org/react";
import Link from "next/link";

const RAGMenu = () => {
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
        <Link
          href="/rags"
          className="text-sm block px-8 py-2 hover:bg-black block text-default-400"
        >
          ☉ RAGS
        </Link>
        <Link
          href="/rags"
          className="text-sm block px-8 py-2 hover:bg-black hover:text-default-200 block text-default-400"
        >
          ☉ RAGS
        </Link>
      </AccordionItem>
    </Accordion>
  );
};

export default RAGMenu;
