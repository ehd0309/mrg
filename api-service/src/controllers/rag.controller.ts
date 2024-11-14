import { LoggerHandler } from "@/middlewares/loggerHandler";
import { Get, JsonController, Param, UseAfter } from "routing-controllers";

import { RagService } from "@/services/rag.service";

@JsonController("/api/rags")
@UseAfter(LoggerHandler)
export class DocumentController {
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
}
