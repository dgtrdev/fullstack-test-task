type ApiErrorResponse = {
  detail?: string;
};


export async function getApiErrorMessage(response: Response, fallbackMessage: string) {
  try {
    const errorData = await response.json() as ApiErrorResponse;

    return errorData.detail || fallbackMessage;
  } catch {
    return fallbackMessage;
  }
}
