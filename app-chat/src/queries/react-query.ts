import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from "@tanstack/react-query";
import type { QueryKey, QueryState } from "@tanstack/react-query";

interface QueryProps<ResponseType = unknown> {
  queryKey: QueryKey;
  queryFn: () => Promise<ResponseType>;
}

export interface DehydratedQuery<TData = unknown, TError = unknown> {
  state: QueryState<TData, TError>;
}

export const getDehydratedQuery = async ({ queryKey, queryFn }: QueryProps) => {
  const queryClient = new QueryClient();
  await queryClient.prefetchQuery({ queryKey, queryFn });
  const state = dehydrate(queryClient);
  return { queryClient, state };
};

export const getDehydratedQueryResult = <TData>({
  queryKey,
  queryClient,
}: {
  queryKey: QueryKey;
  queryClient: QueryClient;
}) => {
  const result = queryClient.getQueryData<TData>(queryKey);
  return result;
};

export const Hydration = HydrationBoundary;
