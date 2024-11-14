import { RetrieveEntity, type RetrieveStatus } from "@/types/model";
import {
  AllowNull,
  Column,
  DataType,
  Default,
  Model,
  Table,
} from "sequelize-typescript";

@Table({
  tableName: "retrieve",
  underscored: true,
})
export class Retrieve extends Model<RetrieveEntity> {
  @AllowNull(false)
  @Default("unknown")
  @Column(DataType.STRING)
  declare model: string;

  @AllowNull(false)
  @Column(DataType.INTEGER)
  declare ragId: number;

  @AllowNull(true)
  @Column(DataType.INTEGER)
  declare responseTime: number;

  @AllowNull(true)
  @Column(DataType.STRING)
  declare question: string;

  @AllowNull(true)
  @Column(DataType.STRING)
  declare answer: string;

  @AllowNull(true)
  @Column(DataType.STRING)
  declare retrievedDocuments: string;

  @AllowNull(false)
  @Default("pending")
  @Column(DataType.STRING)
  declare status: RetrieveStatus;
}
