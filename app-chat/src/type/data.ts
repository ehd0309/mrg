export interface RagInfo {
  ocr_result_paths: string[];
  file_name: string;
  step: string;
  version: "v1" | "v2" | "v3";
}
