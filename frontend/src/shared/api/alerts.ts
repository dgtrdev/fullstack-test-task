import { buildApiUrl } from "../config/api";
import type { AlertItem } from "../types/alerts";
import type { PaginatedResponse } from "../types/pagination";


export async function fetchAlerts() {
  const response = await fetch(buildApiUrl("/alerts"), { cache: "no-store" });

  if (!response.ok) {
    throw new Error("Не удалось загрузить алерты");
  }

  return response.json() as Promise<PaginatedResponse<AlertItem>>;
}
