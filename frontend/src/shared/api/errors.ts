type ApiErrorResponse = {
  detail?: unknown;
};


function formatApiErrorDetail(detail: unknown) {
  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => {
        if (typeof item === "string") {
          return item;
        }

        if (item && typeof item === "object" && "msg" in item && typeof item.msg === "string") {
          return item.msg;
        }

        return null;
      })
      .filter(Boolean);

    return messages.join(", ");
  }

  return "";
}


export async function getApiErrorMessage(response: Response, fallbackMessage: string) {
  try {
    const errorData = await response.json() as ApiErrorResponse;
    const detail = formatApiErrorDetail(errorData.detail);

    return detail || fallbackMessage;
  } catch {
    return fallbackMessage;
  }
}
