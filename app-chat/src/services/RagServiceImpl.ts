import { SERVICE_BACKEND_URL, LC_BACKEND_URL } from "@/constants";
import Service from "@/services/Service";
import { DocumentType } from "@/type/documents";
import { RagType } from "@/type/rags";

class RagService extends Service {
  getList = async () => {
    return this.http.get<RagType[]>("/api/rags", { cache: "no-cache" });
  };
  getById = (id: string) => {
    return this.http.get<RagType>(`/api/rags/${id}`, { cache: "no-cache" });
  };
  initRag = (index_name: string, file_name: string, version: string) => {
    return fetch(LC_BACKEND_URL + `/api/${version}/rags`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      cache: "no-cache",
      body: JSON.stringify({ index_name, file_name }),
    });
  };
  createRag = ({
    name,
    documents,
  }: {
    name: string;
    documents: DocumentType[];
  }) => {
    return this.http.post(
      `/api/rags`,
      { name, documents },
      {
        headers: {
          "Content-Type": "application/json",
        },
        cache: "no-cache",
      }
    ) as Promise<any>;
  };
}

const ragService = new RagService(SERVICE_BACKEND_URL);

export default ragService;
