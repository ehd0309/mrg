import { LoggerHandler } from "@/middlewares/loggerHandler";
import {
  BadRequestError,
  Body,
  Get,
  JsonController,
  Post,
  UploadedFile,
  UseAfter,
} from "routing-controllers";

import { uploadFile } from "@/utils/fileHandler";
import { DocumentService } from "@/services/document.service";

@JsonController("/api/documents")
@UseAfter(LoggerHandler)
export class DocumentController {
  private documentService: DocumentService;

  constructor(documentService: DocumentService) {
    this.documentService = documentService;
  }

  // file upload api
  @Post("")
  async upload(
    @Body()
    {
      name,
      version = "v2",
      description,
    }: { name: string; version?: string; description?: string },
    @UploadedFile("document") document: Express.Multer.File
  ) {
    if (document.mimetype !== "application/pdf") {
      throw new BadRequestError("PDF 파일만 업로드 가능합니다.");
    }
    const filePath = await uploadFile(
      document,
      name,
      "assets/inputs/" + version
    );
    const response = await this.documentService.saveDocumentInfo({
      version,
      documentName: name,
      rawPath: filePath,
      description,
    });
    return { ...response, filePath };
  }
}
