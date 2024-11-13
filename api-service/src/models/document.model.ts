import { DocumentEntity } from "@/types/model";
import {
  AllowNull,
  Column,
  DataType,
  Default,
  Is,
  Length,
  Model,
  Table,
  Unique,
} from "sequelize-typescript";

@Table({
  tableName: "documents",
  underscored: true,
})
export class Document extends Model<DocumentEntity> {
  @AllowNull(false)
  @Is({
    args: /^[a-zA-Z가-힣_][a-zA-Z가-힣0-9_]{4,23}$/,
    msg: "한글 또는 영문으로 시작해야하고 특수문자는 _(언더바)만 허용하며 최대 4~24글자",
  })
  @Unique
  @Column(DataType.STRING)
  declare documentName: string;

  @AllowNull(false)
  @Column(DataType.STRING)
  declare idxName: string;

  @AllowNull(false)
  @Column(DataType.STRING)
  declare rawPath: string;

  @AllowNull(true)
  @Column(DataType.STRING)
  declare ocrPath: string;

  @AllowNull(false)
  @Is({
    args: /^v[0-9]$/,
    msg: "v와 숫자 한자리의 조합",
  })
  @Column(DataType.STRING)
  declare version: string;

  @AllowNull(false)
  @Column(DataType.INTEGER)
  declare pageNum: number;

  @AllowNull(false)
  @Default("default")
  @Column(DataType.STRING)
  declare status: "default" | "uploaded" | "digitized";

  @AllowNull(false)
  @Default(0)
  @Column(DataType.INTEGER)
  declare processedPageCount: number;

  @AllowNull(true)
  @Length({ min: 0, max: 200, msg: "description은 200자 이내" })
  @Column(DataType.STRING)
  declare description: string;
}
