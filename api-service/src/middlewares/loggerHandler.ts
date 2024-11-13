import type { Request } from "express";

import { ExpressMiddlewareInterface } from "routing-controllers";
import { Service } from "typedi";

import { loggerWithRes } from "@/logger";

@Service()
export class LoggerHandler implements ExpressMiddlewareInterface {
  async use(
    request: Request,
    response: any,
    next?: (err?: any) => any
  ): Promise<any> {
    const { originalUrl, method } = request;
    const result = await loggerWithRes(
      {
        level: "info",
        status: response?.statusCode ?? 200,
        method,
        url: originalUrl,
      },
      next
    );
    return result;
  }
}
