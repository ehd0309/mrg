import { createLogger, format, transports } from "winston";
import "winston-daily-rotate-file";

const LOG_DIR = "app-logs";

const loggerFormat = format.combine(
  format.timestamp({
    format: "YYYY-MM-DD HH:mm:ss",
  }),
  format.errors({ stack: true }),
  format.splat(),
  format.printf(
    ({ level, message, timestamp }) =>
      `${timestamp} [${level.toUpperCase()}]: ${message}`
  )
);

const infoLogger = createLogger({
  defaultMeta: { service: "prs-app" },
  format: loggerFormat,
  transports: [
    new transports.DailyRotateFile({
      level: "info",
      filename: `${LOG_DIR}/info-%DATE%.log`,
      datePattern: "YYYY-MM-DD",
      zippedArchive: true,
      maxSize: "20m",
      maxFiles: "7d",
    }),
  ],
});

const errorLogger = createLogger({
  defaultMeta: { service: "prs-app" },
  format: loggerFormat,
  transports: [
    new transports.File({
      level: "error",
      filename: `${LOG_DIR}/error.log`,
      maxsize: 5242880,
    }),
  ],
});

export interface LoggerParams {
  url: string;
  status?: any;
  method: string;
  message?: string;
  res?: string;
}

export const logger = {
  info: ({ url, status, method, message, res }: LoggerParams) =>
    infoLogger.info(
      `[${method}],[${url}],[${status ?? ""}],[${res ?? ""}],[${message ?? ""}]`
    ),
  error: ({ url, status, method, message, res }: LoggerParams) =>
    errorLogger.error(
      `[${method}],[${url}],[${status ?? ""}],[${res ?? ""}],[${message ?? ""}]`
    ),
};

export const loggerWithRes = async <T>(
  params: LoggerParams & { level: "info" | "error" },
  promiseCb?: () => Promise<T>
) => {
  const now = Date.now();
  const response = await promiseCb?.();
  const res = `${Date.now() - now}ms`;
  logger[params.level]({ ...params, res });
  return response;
};
