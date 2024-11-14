export type DocumentStatusType =
  | "default"
  | "uploaded"
  | "pending"
  | "digitized"
  | "embedded"
  | "error";

export enum DocumentStatusEnum {
  "default" = "초기화 되지 않음",
  "uploaded" = "업로드 완료",
  "pending" = "처리 대기",
  "digitized" = "문서 OCR 완료",
  "embedded" = "문서 임베딩 완료",
  "error" = "에러 발생",
}

export type RetrieveStatusType = "pending" | "completed" | "error";

export type VersionType = "v1" | "v2" | "v3";

export interface DocumentType {
  id: number;
  documentName: string;
  idxName: string;
  rawPath: string;
  pageNum: number;
  processedPageCount: number;
  status: DocumentStatusType;
  description: string;
  createdAt: string;
  updatedAt: string;
  version: "v1" | "v2" | "v3";
}

export interface DocumentUploadType {
  document: Blob;
  name: string;
  description: string;
  version?: VersionType;
}
