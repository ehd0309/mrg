"use client";

import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import ReactQueryErrorBoundary from "./ReactQueryErrorBoundary";

import type { FallbackProps } from "react-error-boundary";
import PageTitle from "@/components/PageTitle";
import { Button } from "@nextui-org/react";

const GlobalErrorFallback = ({ error, resetErrorBoundary }: FallbackProps) => {
  const handleRouteButtonClick = () => {
    window.location.href = "/";
  };

  return (
    <div className="bg-black flex flex-col justify-center items-center w-full h-[100dvh] m-auto">
      <div className="flex flex-col justify-center items-center gap-3 mt-[-60px] text-white">
        <h1 className="text-xl font-bold tracking-[0.15rem] leading-[130%] border-gray-100">
          Ooops!
        </h1>
        <PageTitle title="잠시 후 다시 시도해주세요" />
        <p className="text-sm text-gray-400">
          요청을 처리하는데 문제가 생겼습니다.
        </p>
        <div className="flex gap-3">
          <Button
            className="text-black bg-white border"
            variant="light"
            onPress={resetErrorBoundary}
          >
            재시도
          </Button>
          <Button
            className="text-white bg-black border border-white"
            onPress={handleRouteButtonClick}
          >
            홈으로
          </Button>
        </div>
        <p>{JSON.stringify(error)}</p>
      </div>
    </div>
  );
};

export default function ReactQueryProviders({
  children,
}: React.PropsWithChildren) {
  const [queryClient] = useState(() => {
    return new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: 0,
          refetchOnMount: false,
          refetchOnWindowFocus: false,
          refetchInterval: false,
          retry: false,
          refetchOnReconnect: true,
        },
      },
    });
  });

  return (
    <QueryClientProvider client={queryClient}>
      <ReactQueryErrorBoundary fallbackComponent={GlobalErrorFallback}>
        {children}
      </ReactQueryErrorBoundary>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
