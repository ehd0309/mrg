"use client";

import type { ThemeProviderProps } from "next-themes/dist/types";

import { useRouter } from "next/navigation";
import { NextUIProvider } from "@nextui-org/react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import ReactQueryProviders from "@/queries/ReactQueryProvider";
import useDocumentSSE from "@/hooks/useDocumentSSE";

export interface ProvidersProps {
  children: React.ReactNode;
  themeProps?: Omit<ThemeProviderProps, "children">;
}

export function Providers({ children, themeProps }: ProvidersProps) {
  const router = useRouter();

  return (
    <ReactQueryProviders>
      <NextUIProvider navigate={router.push}>
        <NextThemesProvider {...themeProps}>{children}</NextThemesProvider>
      </NextUIProvider>
      <SSE />
    </ReactQueryProviders>
  );
}

export const SSE = () => {
  useDocumentSSE();
  return <></>;
};
