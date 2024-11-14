export type DocumentStatus =
  | "default"
  | "uploaded"
  | "pending"
  | "digitized"
  | "embedded"
  | "error";

export type RetrieveStatus = "pending" | "completed" | "error";

export interface BaseEntity {
  id: string;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface DocumentEntity {
  documentName: string;
  idxName: string;
  rawPath: string;
  ocrPath?: string;
  version: string;
  pageNum: number;
  status: DocumentStatus;
  processedPageCount: number;
  description?: string;
}

export interface RagEntity {
  version: string;
  name: string;
  documents: DocumentEntity[];
  prepareProcessArchtecture?: string;
  retrieveProcessArchtecture?: string;
  description?: string;
}

export interface RetrieveEntity {
  model: string;
  ragId: number;
  responseTime?: number;
  question?: string;
  answer?: string;
  retrievedDocuments?: string;
  status: RetrieveStatus;
}
