import { api } from "@/api";
import Wrapper from "@/app/chat/[id]/_inner/Wrapper";
import Hydrate from "@/components/Hydrate";
import PageLayout from "@/components/PageLayout";
import { useDocumentList } from "@/hooks/useDocuments";
import { useRag } from "@/hooks/useRag";

interface ChatPageProps {
  params: {
    id: string;
  };
}

const ChatPage = async ({ params: { id } }: ChatPageProps) => {
  const prefetch = async () => {
    const { state } = await useRag.prefetch(id);
    return { state };
  };
  const prefetchDocuments = async () => {
    const { state } = await useDocumentList.prefetch();
    return { state };
  };
  return (
    <Hydrate prefetch={prefetchDocuments}>
      <Hydrate prefetch={prefetch}>
        <PageLayout>
          <Wrapper id={id} />
        </PageLayout>
      </Hydrate>
    </Hydrate>
  );
};

export default ChatPage;
