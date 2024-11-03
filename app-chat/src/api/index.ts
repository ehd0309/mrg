import { LC_BACKEND_URL } from "@/constants";
import { RagInfo } from "@/type/data";

export const api = {
  getRagList: async () => {
    const { keys } = await fetch(LC_BACKEND_URL + "/api/v0/rags", {
      cache: "no-cache",
    }).then((res) => res.json());
    return keys as string[];
  },
  getRagById: async (id: string) => {
    const { info } = await fetch(LC_BACKEND_URL + "/api/v0/rags/" + id, {
      cache: "no-cache",
    }).then((res) => res.json());
    return info as RagInfo;
  },
  getRagPipelineById: async (id: string, version: 'v1' | 'v2' | 'v3') => {
    const { pre_process_image, post_process_image } = await fetch(LC_BACKEND_URL + "/api/" + version + "/rags/pipeline/" + id, {
      cache: 'no-cache',
    }).then((res) => res.json());
    return { pre_process_image, post_process_image }
  },
  postRagChat: async (
    id: string,
    question: string,
    version: "v1" | "v2" | "v3"
  ) => {
    const response = await fetch(LC_BACKEND_URL + `/api/${version}/rags/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question, index_name: id }),
    });
    const reader = response?.body?.getReader();
    const decoder = new TextDecoder();
    if (!reader) {
      throw new Error("No reader!");
    }
    return { reader, decoder };
  },
};
