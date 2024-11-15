import { LoggerHandler } from "@/middlewares/loggerHandler";
import {
  Body,
  Get,
  JsonController,
  Param,
  Post,
  UseAfter,
} from "routing-controllers";

import { RagService } from "@/services/rag.service";
import type { CreateRag } from "@/types/transaction";

@JsonController("/api/rags")
@UseAfter(LoggerHandler)
export class RagController {
  private ragService: RagService;

  constructor(ragService: RagService) {
    this.ragService = ragService;
  }

  @Get()
  async getAllRags() {
    return this.ragService.getAllRags();
  }

  @Get("/:id")
  async getRagById(@Param("id") id: string) {
    return this.ragService.getRagById(id);
  }

  @Post()
  async createRag(@Body() rag: Pick<CreateRag, "name" | "documents">) {
    console.log("==================");
    console.log(rag);
    return this.ragService.createRag({ ...rag, version: "v2" } as any);
  }
}
