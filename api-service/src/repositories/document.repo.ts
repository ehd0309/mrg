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

  async getDocumentById(id: number) {
    return await this.documentRepository.findByPk(id);
  }

  async getDocumentByName(documentName: string) {
    return await this.documentRepository.findOne({
      where: { documentName },
    });
  }

  async createDocument(document: CreateDocument) {
    return await this.documentRepository.create(document as Document);
  }
}
