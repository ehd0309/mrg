import sequelize from "@/models";
import { Document } from "@/models/document.model";
import { CreateDocument } from "@/types/transaction";
import { Repository } from "sequelize-typescript";

export class DocumentRepository {
  private documentRepository: Repository<Document>;

  constructor() {
    this.documentRepository = sequelize.getRepository(Document);
  }

  async getAllDocuments() {
    return await this.documentRepository.findAll();
  }

  async getDocumentById(id: string) {
    return await this.documentRepository.findByPk(Number(id), {
      raw: false,
    });
  }

  async getDocumentByName(documentName: string) {
    return await this.documentRepository.findOne({
      where: { documentName },
    });
  }

  async createDocument(document: CreateDocument) {
    return await this.documentRepository.create(document as Document);
  }

  async updateDocument(document: Document) {
    const [_, affected] = await (this.documentRepository as any).update(
      { ...document.dataValues, updatedAt: new Date() },
      {
        where: {
          id: document.id,
        },
        returning: ["id", "updatedAt"],
      }
    );
    return affected?.[0];
  }
}
