import { BaseEntity, DocumentEntity, RagEntity } from "@/types/model";
import { BadRequestError } from "routing-controllers";
import {
  AllowNull,
  Column,
  DataType,
  Default,
  Is,
  Length,
  Model,
  Table,
} from "sequelize-typescript";

@Table({
  tableName: "rag",
  underscored: true,
})
export class Rag extends Model<RagEntity> {
  @AllowNull(false)
  @Column({
    type: DataType.JSON,
    get(this) {
      return JSON.parse(this.getDataValue("documents"));
    },
    set(
      this,
      val: Pick<
        DocumentEntity & BaseEntity,
        "id" | "idxName" | "documentName" | "version"
      >
    ) {
      if (!val.id || !val.idxName || !val.documentName || !val.version) {
        throw new BadRequestError("id, idxName, documentName, version 필수");
      }
      this.setDataValue(
        "documents",
        JSON.stringify([...JSON.parse(this.getDataValue("documents")), val])
      );
    },
  })
  declare documents: Pick<
    DocumentEntity & BaseEntity,
    "id" | "idxName" | "documentName" | "version"
  >[];

  @AllowNull(false)
  @Default("rag")
  @Column(DataType.STRING)
  declare name: string;

  @AllowNull(false)
  @Is({
    args: /^v[0-9]$/,
    msg: "v와 숫자 한자리의 조합",
  })
  @Column(DataType.STRING)
  declare version: string;

  @AllowNull(true)
  @Column(DataType.STRING)
  declare prepareProcessArchtecture: string;

  @AllowNull(true)
  @Column(DataType.STRING)
  declare retrieveProcessArchtecture: string;

  @AllowNull(true)
  @Length({ min: 0, max: 200, msg: "200자 이내" })
  @Column(DataType.STRING)
  declare description: string;
}
