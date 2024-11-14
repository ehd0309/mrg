import { Document } from "@/models/document.model";
import { DocumentRepository } from "@/repositories/document.repo";
import { redisInstance } from "@/services/redis.service";
import { SSEModule } from "@/services/sse.module";
import { RedisChannel } from "@/types/redis";
import { SSEChannel } from "@/types/sse";
import { CreateDocument } from "@/types/transaction";
import {
  archiveFiles,
  getMdFilesFromFolders,
  uploadFile,
} from "@/utils/fileHandler";
import { koreanToRoman } from "@/utils/textHandler";
import { NotFoundError } from "routing-controllers";

export class DocumentService {
  private documentRepository: DocumentRepository;
  private sseModule: SSEModule;
  private redisService = redisInstance();

  constructor(documentRepository: DocumentRepository, sseModule: SSEModule) {
    this.documentRepository = documentRepository;
    this.sseModule = sseModule;
    this.redisService.subscribe(RedisChannel.USER_OCR, async (msg) => {
      if (!msg) {
        return;
      }
      const response = JSON.parse(msg) as Document;
      const document = await this.documentRepository.getDocumentById(
        response.id
      );
      if (!document) {
        throw new NotFoundError("Document not found");
      }
      response?.status && document.set("status", response.status);
      response?.ocrPath && document.set("ocrPath", response.ocrPath);
      response?.pageNum && document.set("pageNum", response.pageNum);
      response?.processedPageCount &&
        document.set("processedPageCount", response.processedPageCount);
      await this.documentRepository.updateDocument(document);
      this.sseModule.emitSSEEvent(
        SSEChannel.DOCUMENT,
        JSON.stringify({ id: document.id })
      );
      if (response?.status === "digitized") {
        this.redisService.publish(
          RedisChannel.LANGCHAIN_EMBED,
          JSON.stringify({ ...document.dataValues })
        );
      }
    });
  }

  async saveDocumentInfo(
    document: Pick<
      CreateDocument,
      "version" | "description" | "documentName"
    > & { file: Express.Multer.File }
  ) {
    const indexName = koreanToRoman(document.documentName);
    const filePath = await uploadFile(
      document.file,
      document.documentName,
      "assets/inputs/" + indexName
    );
    const request: CreateDocument = {
      ...document,
      rawPath: filePath,
      pageNum: 0,
      idxName: indexName,
      status: "uploaded",
    };
    const response = await this.documentRepository.createDocument({
      ...request,
    });
    this.redisService.publish(
      RedisChannel.DOCUMENT,
      JSON.stringify({ ...response.dataValues, version: document.version })
    );
    return {
      id: response.id,
      createdAt: response.createdAt,
      index: response.idxName,
      filePath,
    };
  }

  async getAllDocuments() {
    return this.documentRepository.getAllDocuments();
  }

  async getDocumentById(id: string) {
    return this.documentRepository.getDocumentById(id);
  }

  async getDocumentFileById(id: string, isOutput: boolean, res: any) {
    const document = await this.documentRepository.getDocumentById(id);
    let outputPath: string[] = [];
    if (isOutput) {
      const folder_path = (document?.ocrPath ?? "")
        .replaceAll("\\", "/")
        .split(",");
      outputPath = await getMdFilesFromFolders(folder_path);
    } else {
      outputPath = [document?.rawPath ?? ""];
    }
    await archiveFiles(outputPath, res);
  }
}
