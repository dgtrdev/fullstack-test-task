import { describe, expect, it } from "vitest";

import { getApiErrorMessage } from "./errors";


describe("getApiErrorMessage", () => {
  it("возвращает строковую причину из detail", async () => {
    const response = new Response(JSON.stringify({ detail: "File is empty" }), {
      status: 400,
    });

    await expect(getApiErrorMessage(response, "Неизвестная ошибка")).resolves.toBe("File is empty");
  });

  it("собирает сообщения FastAPI validation errors", async () => {
    const response = new Response(
      JSON.stringify({
        detail: [
          { msg: "Field required" },
          { msg: "Input should be greater than or equal to 1" },
        ],
      }),
      { status: 422 },
    );

    await expect(getApiErrorMessage(response, "Неизвестная ошибка")).resolves.toBe(
      "Field required, Input should be greater than or equal to 1",
    );
  });

  it("возвращает fallback, если ответ не JSON", async () => {
    const response = new Response("Server error", { status: 500 });

    await expect(getApiErrorMessage(response, "Неизвестная ошибка")).resolves.toBe("Неизвестная ошибка");
  });
});
