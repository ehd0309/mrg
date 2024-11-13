import { DocumentRepository } from "@/repositories/document.repo";
import { CreateDocument } from "@/types/transaction";
import { koreanToRoman } from "@/utils/textHandler";

export class DocumentService {
  private documentRepository: DocumentRepository;

  constructor(documentRepository: DocumentRepository) {
    this.documentRepository = documentRepository;
  }

  async saveDocumentInfo(
    document: Pick<
      CreateDocument,
      "rawPath" | "version" | "description" | "documentName"
    >
  ) {
    const request: CreateDocument = {
      ...document,
      pageNum: 0,
      idxName: koreanToRoman(document.documentName),
    };
    const response = await this.documentRepository.createDocument(request);
    return { id: response.id, createdAt: response.createdAt };
  }
}
