import { SERVICE_BACKEND_URL, LC_BACKEND_URL } from "@/constants";
import Service from "@/services/Service";
import { DocumentType, DocumentUploadType } from "@/type/documents";
import { RagType } from "@/type/rags";

class RagService extends Service {
  getList = async () => {
    return this.http.get<RagType[]>("/api/rags");
  };
  getById = (id: string) => {
    return this.http.get<DocumentType>(`/api/rags/${id}`);
  };
  initRag = (index_name: string, file_name: string, version: string) => {
    return fetch(LC_BACKEND_URL + `/api/${version}/rags`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ index_name, file_name }),
    });
  };
}

const ragService = new RagService(SERVICE_BACKEND_URL);

export default ragService;
