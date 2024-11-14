import { LoggerHandler } from "@/middlewares/loggerHandler";
import {
  BadRequestError,
  Body,
  Get,
  JsonController,
  Param,
  Post,
  Res,
  UploadedFile,
  UseAfter,
} from "routing-controllers";

import { DocumentService } from "@/services/document.service";

import type { Response } from "express";

@JsonController("/api/documents")
@UseAfter(LoggerHandler)
export class DocumentController {
  private documentService: DocumentService;

  constructor(documentService: DocumentService) {
    this.documentService = documentService;
  }

  // file upload api
  @Post()
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
    const response = await this.documentService.saveDocumentInfo({
      version,
      documentName: name,
      description,
      file: document,
    });
    return { ...response, version };
  }

  @Get()
  async getAllDocuments() {
    return this.documentService.getAllDocuments();
  }

  @Get("/:id")
  async getDocumentById(@Param("id") id: string) {
    return this.documentService.getDocumentById(id);
  }

  @Get("/:id/file/raw")
  async getRawDocumentFile(@Param("id") id: string, @Res() res: Response) {
    return await this.documentService.getDocumentFileById(id, false, res);
  }

  @Get("/:id/file/output")
  async getOutputDocumentFile(@Param("id") id: string, @Res() res: Response) {
    return await this.documentService.getDocumentFileById(id, true, res);
  }
}
