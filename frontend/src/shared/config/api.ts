const rawApiBaseUrl = process.env.NEXT_PUBLIC_API_URL;

if (!rawApiBaseUrl) {
  throw new Error("Не задана переменная окружения NEXT_PUBLIC_API_URL");
}

export const API_BASE_URL = rawApiBaseUrl.replace(/\/+$/, "");

export function buildApiUrl(path: string) {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;

  return `${API_BASE_URL}${normalizedPath}`;
}
