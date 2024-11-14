import type { Response } from "express";
import { EventEmitter } from "events";

import { logger } from "@/logger";
import { SSEChannel } from "@/types/sse";

export class SSEModule {
  private emitter: EventEmitter;
  private connectedCnt: number;

  constructor() {
    this.emitter = new EventEmitter();
    this.connectedCnt = 0;
  }

  public onSSE = (res: Response, eventName: SSEChannel) => {
    this.connectedCnt = this.connectedCnt + 1;
    this.emitter.on(eventName, ({ data }) => {
      logger.info({
        url: "SSE",
        method: "GET",
        message: `{${eventName}}: receive message`,
      });
      res.write(`event: ${eventName}\n`);
      res.write(`data: ${JSON.stringify(data)}\n\n`);
    });
  };

  public emitSSEEvent = (eventName: SSEChannel, message: string) => {
    this.emitter.emit(eventName, { data: message });
  };

  public offSSE = (res: Response, eventName: SSEChannel) => {
    this.emitter.removeAllListeners(eventName);
    this.connectedCnt = this.connectedCnt - 1;
    res.write("event: disconnected\n");
    res.write("message: disconnected!\n");
  };

  public connectedInfoMessage = () => {
    return `${this.connectedCnt} events connected`;
  };
}
