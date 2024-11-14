import { ApiError } from "@/services/ApiError";

interface HTTPMethod {
  get<T>(url: string, config?: RequestInit): Promise<T>;
  delete<T>(url: string, config?: RequestInit): Promise<T>;
  post<T>(url: string, data?: unknown, config?: RequestInit): Promise<T>;
  put<T>(url: string, data?: unknown, config?: RequestInit): Promise<T>;
  patch<T>(url: string, data?: unknown, config?: RequestInit): Promise<T>;
}

class Service {
  public http: HTTPMethod;

  public baseURL: string;

  private headers: Record<string, string>;

  constructor(baseURL?: string) {
    this.baseURL = baseURL ?? "http://localhost:8000";
    this.headers = {};

    this.http = {
      get: this.get.bind(this),
      delete: this.delete.bind(this),
      post: this.post.bind(this),
      put: this.put.bind(this),
      patch: this.patch.bind(this),
    };
  }

  private async request<T = unknown>(
    method: string,
    url: string,
    data?: unknown,
    config?: RequestInit
  ): Promise<T> {
    const _header = {
      ...this.headers,
      ...config?.headers,
    };
    try {
      const response = await fetch(this.baseURL + url, {
        method,
        ...config,
        headers: _header,
        body: data ? JSON.stringify(data) : undefined,
        cache: config?.cache ?? "no-cache",
      });
      if (!response.ok) {
        const error: ApiError = await response.json();
        throw new ApiError(error.message, error.code);
      }
      const responseData: T = await response.json();
      return responseData;
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error("Error:", error);
      throw error;
    }
  }

  private get<T>(url: string, config?: RequestInit): Promise<T> {
    return this.request<T>("GET", url, undefined, config);
  }

  private delete<T>(url: string, config?: RequestInit): Promise<T> {
    return this.request<T>("DELETE", url, undefined, config);
  }

  private post<T>(
    url: string,
    data?: unknown,
    config?: RequestInit
  ): Promise<T> {
    return this.request<T>("POST", url, data, config);
  }

  private put<T>(
    url: string,
    data?: unknown,
    config?: RequestInit
  ): Promise<T> {
    return this.request<T>("PUT", url, data, config);
  }

  private patch<T>(
    url: string,
    data?: unknown,
    config?: RequestInit
  ): Promise<T> {
    return this.request<T>("PATCH", url, data, config);
  }
}

export default Service;
