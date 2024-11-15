import { DocumentController } from "@/controllers/document.controller";
import { RagController } from "@/controllers/rag.controller";
import { SSEController } from "@/controllers/sse.controller";
import { DocumentRepository } from "@/repositories/document.repo";
import { RagRepository } from "@/repositories/rag.repo";
import { RetrieveRepository } from "@/repositories/retrieve.repo";
import { DocumentService } from "@/services/document.service";
import { RagService } from "@/services/rag.service";
import { RedisService } from "@/services/redis.service";
import { SSEModule } from "@/services/sse.module";
import { Container } from "typedi";

export const container = Container;

Container.set(DocumentRepository, new DocumentRepository());
Container.set(RagRepository, new RagRepository());
Container.set(RetrieveRepository, new RetrieveRepository());

Container.set(SSEModule, new SSEModule());
Container.set(RedisService, new RedisService());
Container.set(
  DocumentService,
  new DocumentService(
    Container.get(DocumentRepository),
    Container.get(RagRepository),
    Container.get(SSEModule)
  )
);
Container.set(RagService, new RagService(Container.get(RagRepository)));

Container.set(SSEController, new SSEController(Container.get(SSEModule)));
Container.set(
  DocumentController,
  new DocumentController(Container.get(DocumentService))
);

Container.set(RagController, new RagController(Container.get(RagService)));

export const controllers = [DocumentController, RagController, SSEController];
