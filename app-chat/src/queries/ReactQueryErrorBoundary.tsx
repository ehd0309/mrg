import { ErrorBoundary } from "react-error-boundary";
import type { FallbackProps } from "react-error-boundary";
import { QueryErrorResetBoundary } from "@tanstack/react-query";

interface QueryErrorBoundaryProps {
  children: React.ReactNode;
  fallbackComponent: (props: FallbackProps) => React.ReactNode;
}

const ReactQueryErrorBoundary = ({
  children,
  fallbackComponent,
}: QueryErrorBoundaryProps) => {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary onReset={reset} fallbackRender={fallbackComponent}>
          {children}
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
};

export default ReactQueryErrorBoundary;
