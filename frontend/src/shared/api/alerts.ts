import { buildApiUrl } from "../config/api";
import type { AlertItem } from "../types/alerts";
import type { PaginatedResponse, PaginationParams } from "../types/pagination";


export async function fetchAlerts({ limit, offset }: PaginationParams) {
  const searchParams = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });
  const response = await fetch(buildApiUrl(`/alerts?${searchParams.toString()}`), { cache: "no-store" });

  if (!response.ok) {
    throw new Error("Не удалось загрузить алерты");
  }

  return response.json() as Promise<PaginatedResponse<AlertItem>>;
}
