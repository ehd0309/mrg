import { queryKeys } from "@/queries/keys";
import {
  getDehydratedQuery,
  getDehydratedQueryResult,
} from "@/queries/react-query";
import ragService from "@/services/RagServiceImpl";
import { RagType } from "@/type/rags";
import { useSuspenseQuery } from "@tanstack/react-query";

const LIST_OPTION = () => ({
  queryKey: queryKeys.rag.list(),
  queryFn: ragService.getList,
});

export const useRagList = () => {
  const { data } = useSuspenseQuery({ ...LIST_OPTION() });

  return { documents: data };
};

useRagList.prefetch = async () => {
  const { state, queryClient } = await getDehydratedQuery(LIST_OPTION());
  const dataRequestList = getDehydratedQueryResult<RagType[]>({
    queryKey: LIST_OPTION().queryKey,
    queryClient,
  });
  return { state, queryClient, dataRequestList: dataRequestList ?? [] };
};

const DOCUMENT_OPTION = (id: string) => ({
  queryKey: queryKeys.rag.byId(id),
  queryFn: () => ragService.getById(id),
});

export const useRag = (id: string) => {
  const { data } = useSuspenseQuery({ ...DOCUMENT_OPTION(id) });

  return { document: data };
};

useRag.prefetch = async (id: string) => {
  const { state, queryClient } = await getDehydratedQuery(DOCUMENT_OPTION(id));
  const dataRequest = getDehydratedQueryResult<DocumentType>({
    queryKey: DOCUMENT_OPTION(id).queryKey,
    queryClient,
  });
  return { state, queryClient, dataRequest };
};
