import { RagRepository } from "@/repositories/rag.repo";
import { CreateRag } from "@/types/transaction";

export class RagService {
  private ragRepository: RagRepository;

  constructor(ragRepository: RagRepository) {
    this.ragRepository = ragRepository;
  }

  async getAllRags() {
    return await this.ragRepository.getAllRags();
  }

  async getRagById(id: string) {
    return await this.ragRepository.getRagById(Number(id));
  }

  async createRag(rag: CreateRag) {
    return await this.ragRepository.createRag(rag);
  }
}
