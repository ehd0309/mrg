FROM node:18-alpine AS base

RUN apk add --no-cache libc6-compat bash
RUN apk update
RUN corepack enable
COPY . /app
WORKDIR /app



FROM base AS client-build

ARG LANGCHAIN_BACKEND_URL

RUN pnpm install
RUN echo "NEXT_PUBLIC_LANGCHAIN_BACKEND=${LANGCHAIN_BACKEND_URL}" > env && \
    echo "TZ=Asia/Seoul" >> env
RUN cp env .env
RUN pnpm build



FROM node:18-alpine AS client-runner
RUN apk add --no-cache bash
WORKDIR /app

COPY --from=client-build /app/next.config.js .
COPY --from=client-build /app/package.json .
COPY --from=client-build /app/.env .

COPY --from=client-build /app/.next/standalone ./
COPY --from=client-build /app/.next/static ./.next/static
COPY --from=client-build /app/public ./public

EXPOSE 3333
ENV PORT 3333

CMD node server.js
