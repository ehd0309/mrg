import sequelize from "@/models";
import { Rag } from "@/models/rag.model";
import { CreateRag } from "@/types/transaction";
import { Repository } from "sequelize-typescript";

export class RagRepository {
  private ragRepository: Repository<Rag>;

  constructor() {
    this.ragRepository = sequelize.getRepository(Rag);
  }

  async getAllRags() {
    return await this.ragRepository.findAll();
  }

  async getRagById(id: number) {
    return await this.ragRepository.findByPk(id);
  }

  async createRag(rag: CreateRag) {
    return await this.ragRepository.create(rag);
  }
}
