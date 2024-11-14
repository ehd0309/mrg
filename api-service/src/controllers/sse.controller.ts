import type { Request, Response } from "express";

import { Controller, Get, Req, Res } from "routing-controllers";

import { logger } from "@/logger";
import { SSEModule } from "@/services/sse.module";
import { SSEChannel } from "@/types/sse";

export const SSE_HEADERS = {
  "Content-Type": "text/event-stream",
  Connection: "keep-alive",
  "Cache-Control": "no-cache",
};

@Controller("/sse")
export class SSEController {
  private sseService: SSEModule;

  constructor(sseService: SSEModule) {
    this.sseService = sseService;
  }

  @Get("/documents")
  connect(@Req() request: Request, @Res() response: Response) {
    response.writeHead(200, SSE_HEADERS);
    response.write("event: start\n");
    response.write("message: connected!\n");

    this.sseService.onSSE(response, SSEChannel.DOCUMENT);
    logger.info({
      url: "/sse/documents",
      method: "GET",
      message: `{documents}: connected, {CNT}: ${this.sseService.connectedInfoMessage()}`,
    });

    request.on("close", () => {
      this.sseService.offSSE(response, SSEChannel.DOCUMENT);
      logger.info({
        url: "/sse/documents",
        method: "GET",
        message: `{documents}: disconnected, {CNT}: ${this.sseService.connectedInfoMessage()}`,
      });
    });
    return response;
  }
}
