import DocumentMenu from "@/components/DocumentMenu";
import DocumentUploader from "@/components/DocumentUploader";
import Hydrate from "@/components/Hydrate";
import RAGMenu from "@/components/RAGMenu";
import { useDocumentList } from "@/hooks/useDocuments";
import { Divider } from "@nextui-org/react";
import Link from "next/link";

const Sidebar = async () => {
  const prefetchDocuments = async () => {
    const { state } = await useDocumentList.prefetch();
    return { state };
  };
  return (
    <div
      className="bg-default-800 text-white py-4 flex flex-col justify-between min-h-[calc(100dvh)]"
      style={{ position: "sticky", left: 0, top: 0 }}
    >
      <div className="flex flex-col gap-2">
        <div className="flex flex-col gap-3">
          <Hydrate prefetch={prefetchDocuments}>
            <DocumentMenu />
          </Hydrate>
          <RAGMenu />
        </div>
      </div>
      <div
        className="flex flex-col gap-2"
        style={{ transform: "translateY(-52px)" }}
      >
        <Divider className="bg-primary-200" />
        <br />
        <div className="px-10">
          <DocumentUploader />
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
