import { queryKeys } from "@/queries/keys";
import {
  getDehydratedQuery,
  getDehydratedQueryResult,
} from "@/queries/react-query";
import documentService from "@/services/DocumentServiceImpl";
import { DocumentType } from "@/type/documents";
import { useQuery, useSuspenseQuery } from "@tanstack/react-query";

const LIST_OPTION = () => ({
  queryKey: queryKeys.documents.list(),
  queryFn: documentService.getList,
});

export const useDocumentList = () => {
  const { data } = useSuspenseQuery({ ...LIST_OPTION() });

  return { documents: data };
};

useDocumentList.prefetch = async () => {
  const { state, queryClient } = await getDehydratedQuery(LIST_OPTION());
  const dataRequestList = getDehydratedQueryResult<DocumentType[]>({
    queryKey: LIST_OPTION().queryKey,
    queryClient,
  });
  return { state, queryClient, dataRequestList: dataRequestList ?? [] };
};

const DOCUMENT_OPTION = (id: string) => ({
  queryKey: queryKeys.documents.byId(id),
  queryFn: () => documentService.getDocument(id),
});

export const useDocument = (id: string) => {
  const { data } = useSuspenseQuery({ ...DOCUMENT_OPTION(id) });

  return { document: data };
};

useDocument.prefetch = async (id: string) => {
  const { state, queryClient } = await getDehydratedQuery(DOCUMENT_OPTION(id));
  const dataRequest = getDehydratedQueryResult<DocumentType>({
    queryKey: DOCUMENT_OPTION(id).queryKey,
    queryClient,
  });
  return { state, queryClient, dataRequest };
};

export const useDocumentRawFile = (id: string, isEnable?: boolean) => {
  const { data, isLoading, isError } = useQuery({
    queryKey: queryKeys.documents.inputFile(id),
    queryFn: () => documentService.getRawFile(id),
    enabled: isEnable,
  });

  return { rawFiles: data, isLoading, isError };
};

export const useDocumentOutputFile = (id: string, isEnable?: boolean) => {
  const { data, isLoading, isError } = useQuery({
    queryKey: queryKeys.documents.outputFile(id),
    queryFn: () => documentService.getOCRFile(id),
    enabled: isEnable,
  });

  return { outputFiles: data, isLoading, isError };
};
