import { SERVICE_BACKEND_URL } from "@/constants";
import Service from "@/services/Service";
import { DocumentType, DocumentUploadType } from "@/type/documents";
import JSZip from "jszip";

class DocumentService extends Service {
  getList = async () => {
    return this.http.get<DocumentType[]>("/api/documents", {
      cache: "no-cache",
    });
  };
  upload = ({
    document,
    description,
    name,
    version = "v2",
  }: DocumentUploadType) => {
    const formData = new FormData();
    formData.append("document", document);
    formData.append("name", name);
    formData.append("description", description);
    formData.append("version", version);
    return fetch(`${this.baseURL}/api/documents`, {
      method: "POST",
      body: formData,
      cache: "no-cache",
    }).then((res) => res.json()) as Promise<
      Pick<DocumentType, "id" | "idxName" | "version">
    >;
  };
  getDocument = (id: string) => {
    return this.http.get<DocumentType>(`/api/documents/${id}`, {
      cache: "no-cache",
    });
  };
  getRawFile = async (id: string) => {
    const response = await fetch(
      `${this.baseURL}/api/documents/${id}/file/raw`,
      { cache: "no-cache" }
    );
    const blob = await response.blob();
    const zip = await JSZip.loadAsync(blob);
    const pdfFiles = await Promise.all(
      Object.keys(zip.files).map(async (relativePath) => {
        const file = zip.files[relativePath];
        const pdfBlob = await file.async("blob");
        return URL.createObjectURL(pdfBlob);
      })
    );
    return pdfFiles;
  };

  getOCRFile = async (id: string) => {
    const response = await fetch(
      `${this.baseURL}/api/documents/${id}/file/output`,
      { cache: "no-cache" }
    );
    const blob = await response.blob();
    const zip = await JSZip.loadAsync(blob);
    const pdfFiles = await Promise.all(
      Object.keys(zip.files).map(async (relativePath) => {
        const file = zip.files[relativePath];
        const mdTexts = await file.async("text");
        return mdTexts;
      })
    );
    return pdfFiles;
  };
}

const documentService = new DocumentService(SERVICE_BACKEND_URL);

export default documentService;
