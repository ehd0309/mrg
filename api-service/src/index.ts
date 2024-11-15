import "reflect-metadata";

import cors from "cors";
import bodyParser from "body-parser";
import cookieParser from "cookie-parser";
import express from "express";
import { useContainer, useExpressServer } from "routing-controllers";
import dotEnv from "dotenv";

import { controllers, container } from "@/controllers";
import { ErrorHandler } from "@/middlewares/errorHandler";
import { logger } from "@/logger";

import sequelize from "./models";
import { redisInstance } from "@/services/redis.service";

const PORT = 4000;

dotEnv.config();

const app = express();
// app.use(
//   cors({
//     allowedHeaders: ["*"],
//     origin: ["http://localhost:3000"],
//   })
// );
app.use(bodyParser.json());
app.use(cookieParser());

async function initializeDatabaseAndServer() {
  try {
    await sequelize.sync();
    logger.info({
      url: "BASE",
      method: "NONE",
      message: "App Database connected and synchronized successfully",
    });
    useContainer(container);

    useExpressServer(app, {
      controllers: controllers,
      defaultErrorHandler: false,
      middlewares: [ErrorHandler],
      classTransformer: false,
      cors: true,
    });

    const redis = redisInstance();
    await redis.initialize();

    app.listen(PORT, () => {
      logger.info({
        url: "BASE",
        method: "NONE",
        message: `App Server connected with port ${PORT}`,
      });
    });
  } catch (error) {
    logger.error({
      url: "BASE",
      method: "NONE",
      message: `Unable to connect to the database with ${error}`,
    });
    process.exit(1);
  }
}

initializeDatabaseAndServer();
