import { SERVICE_BACKEND_URL } from "@/constants";
import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { queryKeys } from "@/queries/keys";

const useDocumentSSE = () => {
  const queryClient = useQueryClient();

  useEffect(() => {
    const createdEventSource = new EventSource(
      SERVICE_BACKEND_URL + "/sse/documents"
    );

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const eventListener = (e: MessageEvent<any>) => {
      console.log(e);
      queryClient.invalidateQueries({
        queryKey: queryKeys.documents.list(),
        exact: false,
      });
    };
    createdEventSource.addEventListener("DOCUMENT", eventListener);

    return () => {
      createdEventSource.removeEventListener("DOCUMENT", eventListener);
    };

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queryClient]);
};

export default useDocumentSSE;
