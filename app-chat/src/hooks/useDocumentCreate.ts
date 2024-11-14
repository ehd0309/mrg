"use client";

import { queryKeys } from "@/queries/keys";
import documentService from "@/services/DocumentServiceImpl";
import { useMutation, useQueryClient } from "@tanstack/react-query";

const useDocumentCreate = () => {
  const queryClient = useQueryClient();
  const { mutateAsync } = useMutation({
    mutationFn: documentService.upload,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.documents.list(),
      });
    },
  });
  return { createDocument: mutateAsync };
};

export default useDocumentCreate;
