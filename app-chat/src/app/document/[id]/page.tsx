import BaseInfo from "@/app/document/[id]/_inner/BaseInfo";
import Hydrate from "@/components/Hydrate";
import PageLayout from "@/components/PageLayout";
import { useDocument } from "@/hooks/useDocuments";

interface DocumentPageProps {
  params: {
    id: string;
  };
}

const DocumentPage = async ({ params: { id } }: DocumentPageProps) => {
  const prefetch = async () => {
    const { state } = await useDocument.prefetch(id);
    return { state };
  };

  return (
    <PageLayout>
      <Hydrate prefetch={prefetch}>
        <BaseInfo id={id} />
      </Hydrate>
    </PageLayout>
  );
};

export default DocumentPage;
