import { Sequelize } from "sequelize-typescript";

import configData from "../config/db-config";
import { Document } from "@/models/document.model";
import { Rag } from "@/models/rag.model";
import { Retrieve } from "@/models/retrieve.model";

const configs = configData;
const env = process.env.NODE_ENV || "development";
const config = configs[env];

interface DB {
  [key: string]: any;
  sequelize?: Sequelize;
}

const db: DB = {};

const sequelize = new Sequelize({
  ...config,
  repositoryMode: true,
  query: {
    raw: true,
  },
  password: config.password === null ? undefined : config.password,
  models: [Document, Rag, Retrieve],
});

db.sequelize = sequelize;

export default sequelize;
