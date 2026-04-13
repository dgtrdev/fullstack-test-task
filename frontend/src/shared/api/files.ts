import { buildApiUrl } from "../config/api";
import type { FileItem } from "../types/files";
import type { PaginatedResponse, PaginationParams } from "../types/pagination";


export async function fetchFiles({ limit, offset }: PaginationParams) {
  const searchParams = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });
  const response = await fetch(buildApiUrl(`/files?${searchParams.toString()}`), { cache: "no-store" });

  if (!response.ok) {
    throw new Error("Не удалось загрузить файлы");
  }

  return response.json() as Promise<PaginatedResponse<FileItem>>;
}


export async function uploadFile(title: string, file: File) {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("file", file);

  const response = await fetch(buildApiUrl("/files"), {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Не удалось загрузить файл");
  }

  return response.json() as Promise<FileItem>;
}


export function getFileDownloadUrl(fileId: string) {
  return buildApiUrl(`/files/${fileId}/download`);
}
