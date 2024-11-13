import { DocumentController } from "@/controllers/document.controller";
import { DocumentRepository } from "@/repositories/document.repo";
import { DocumentService } from "@/services/document.service";
import { Container } from "typedi";

export const container = Container;

Container.set(DocumentRepository, new DocumentRepository());
Container.set(
  DocumentService,
  new DocumentService(Container.get(DocumentRepository))
);

Container.set(
  DocumentController,
  new DocumentController(Container.get(DocumentService))
);

export const controllers = [DocumentController];
