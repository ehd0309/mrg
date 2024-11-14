import { DocumentEntity, RagEntity, RetrieveEntity } from "@/types/model";

export interface CreateDocument
  extends Omit<DocumentEntity, "id" | "processedPageCount"> {}

export interface CreateRag
  extends Omit<
    RagEntity,
    "prepareProcessArchtecture" | "retrieveProcessArchtecture"
  > {}

export interface CreateRetrieve extends Omit<RetrieveEntity, "status"> {}