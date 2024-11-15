import DocumentMenu from "@/components/DocumentMenu";
import DocumentUploader from "@/components/DocumentUploader";
import Hydrate from "@/components/Hydrate";
import RAGMenu from "@/components/RAGMenu";
import RagUploader from "@/components/RagUploader";
import { useDocumentList } from "@/hooks/useDocuments";
import { useRagList } from "@/hooks/useRag";
import { Divider } from "@nextui-org/react";

const Sidebar = async () => {
  const prefetchDocuments = async () => {
    const { state } = await useDocumentList.prefetch();
    return { state };
  };
  const prefetchRags = async () => {
    const { state } = await useRagList.prefetch();
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
          <Hydrate prefetch={prefetchRags}>
            <RAGMenu />
          </Hydrate>
        </div>
      </div>
      <div
        className="flex flex-col gap-2"
        style={{ transform: "translateY(-52px)" }}
      >
        <Divider className="bg-primary-200 mb-2" />
        <Hydrate prefetch={prefetchDocuments}>
          <div className="px-6 flex flex-col gap-4">
            <DocumentUploader />
            <RagUploader />
          </div>
        </Hydrate>
      </div>
    </div>
  );
};

export default Sidebar;
