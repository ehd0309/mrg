import { DocumentController } from "@/controllers/document.controller";
import { SSEController } from "@/controllers/sse.controller";
import { DocumentRepository } from "@/repositories/document.repo";
import { DocumentService } from "@/services/document.service";
import { RedisService } from "@/services/redis.service";
import { SSEModule } from "@/services/sse.module";
import { Container } from "typedi";

export const container = Container;

Container.set(DocumentRepository, new DocumentRepository());

Container.set(SSEModule, new SSEModule());
Container.set(RedisService, new RedisService());
Container.set(
  DocumentService,
  new DocumentService(
    Container.get(DocumentRepository),
    Container.get(SSEModule)
  )
);

Container.set(SSEController, new SSEController(Container.get(SSEModule)));
Container.set(
  DocumentController,
  new DocumentController(Container.get(DocumentService))
);

export const controllers = [DocumentController, SSEController];
