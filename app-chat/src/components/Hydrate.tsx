import { Suspense } from "react";

import { Hydration } from "@/queries/react-query";
import type { DehydratedState } from "@tanstack/react-query";
import { notFound } from "next/navigation";

interface HydrateProps {
  children: React.ReactNode;
  prefetch: () => Promise<{ state: DehydratedState }>;
}

const Hydrate = async ({ children, prefetch }: HydrateProps) => {
  const isBuildTime = process.env.NEXT_PHASE === "PHASE_PRODUCTION_BUILD";
  const { state } = isBuildTime
    ? { state: { queries: [], mutations: [] } }
    : await prefetch();
  if (state.queries.length === 0) {
    notFound();
  }
  return (
    <Hydration state={state}>
      <Suspense>{children}</Suspense>
    </Hydration>
  );
};

export default Hydrate;
