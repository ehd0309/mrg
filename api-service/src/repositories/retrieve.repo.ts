import sequelize from "@/models";
import { Retrieve } from "@/models/retrieve.model";
import { Repository } from "sequelize-typescript";

export class RetrieveRepository {
  private retrieveRepository: Repository<Retrieve>;

  constructor() {
    this.retrieveRepository = sequelize.getRepository(Retrieve);
  }

  async getAllRetrieves() {
    return await this.retrieveRepository.findAll();
  }

  async getRetrieveById(id: number) {
    return await this.retrieveRepository.findByPk(id);
  }

  async createRetrieve(retrieve: Retrieve) {
    return await this.retrieveRepository.create(retrieve);
  }
}
