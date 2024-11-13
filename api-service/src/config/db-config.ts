import type { Dialect } from "sequelize";

import dotenv from "dotenv";

dotenv.config();

export interface DBEnvConfig {
  database?: string;
  username?: string;
  password?: string | null | undefined;
  host?: string;
  dialect: Dialect;
  storage?: any;
}

export interface DBConfig {
  [env: string]: DBEnvConfig;
}

const config: DBConfig = {
  development: {
    dialect: "sqlite",
    storage: "database.sqlite3",
  },
  test: {
    dialect: "sqlite",
    storage: ":memory",
  },
  production: {
    username: process.env.DB_USERNAME,
    password: process.env.DB_PASSWORD,
    database: "prsapp",
    host: process.env.DB_HOST,
    dialect: "postgres",
  },
};

export default config;
