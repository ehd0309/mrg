"use client";

import { queryKeys } from "@/queries/keys";
import ragService from "@/services/RagServiceImpl";
import { useMutation, useQueryClient } from "@tanstack/react-query";

const useRagCreate = () => {
  const queryClient = useQueryClient();
  const { mutateAsync } = useMutation({
    mutationFn: ragService.createRag,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.rag.list(),
      });
    },
  });
  return { createRag: mutateAsync };
};

export default useRagCreate;
