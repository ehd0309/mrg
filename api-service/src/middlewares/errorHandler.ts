import {
  Middleware,
  ExpressErrorMiddlewareInterface,
  HttpError,
} from "routing-controllers";
import { Request, Response } from "express";
import { Service } from "typedi";

import { logger } from "@/logger";

@Middleware({ type: "after" })
@Service()
export class ErrorHandler implements ExpressErrorMiddlewareInterface {
  error(error: HttpError | Error, req: Request, res: Response) {
    const { originalUrl, method } = req;
    if (error instanceof HttpError) {
      const { httpCode, message } = error;
      logger.error({ url: originalUrl, method, status: httpCode, message });
      res.status(error.httpCode).send({ code: httpCode, message });
      return;
    }

    if (error.name === "SequelizeValidationError") {
      const message = error.message ?? "bad input request";
      logger.error({ url: originalUrl, status: 400, method, message });
      res.status(400).send({ code: 400, message });
      return;
    }

    if (error.name.startsWith("Sequelize")) {
      const message = error.message ?? "bad input request";
      logger.error({
        url: originalUrl,
        status: 555,
        method,
        message: (error as any)?.errors?.[0]?.message ?? message,
      });
      res.status(500).send({ code: 555, message: message });
      return;
    }

    logger.error({
      url: originalUrl,
      status: 500,
      method,
      message: error?.message ?? "UNHANDLED ERROR!!",
    });
    res.status(500).send({ code: 500, error: "Internal Server Error" });
  }
}
