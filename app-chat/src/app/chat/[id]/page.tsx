import { api } from "@/api";
import Wrapper from "@/app/chat/[id]/_inner/Wrapper";
import PageLayout from "@/components/PageLayout";
import PageTitle from "@/components/PageTitle";
import { notFound } from "next/navigation";

interface ChatPageProps {
  params: {
    id: string;
  };
}

const ChatPage = async ({ params: { id } }: ChatPageProps) => {
  const info = await api.getRagById(id);
  if (!info || !info?.file_name) {
    notFound();
  }
  return (
    <PageLayout>
      <PageTitle title={info.file_name} />
      <Wrapper id={id} version={info.version} />
    </PageLayout>
  );
};

export default ChatPage;
