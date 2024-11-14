### base phase
FROM node:18-alpine AS base

RUN apk update
RUN apk add --no-cache libc6-compat
RUN corepack enable

WORKDIR /app

COPY . .

RUN pnpm install

RUN pnpm build

ENV PORT 8000

CMD ["pnpm", "start"]