import { DocumentType } from "@/type/documents";

export interface RagType {
  id: number;
  name: string;
  documents: DocumentType[];
  prepareProcessArchtecture?: string;
  retrieveProcessArchtecture?: string;
  description?: string;
  version: "v1" | "v2" | "v3";
  idxName: string;
}
