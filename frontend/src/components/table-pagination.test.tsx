import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { TablePagination } from "./table-pagination";


describe("TablePagination", () => {
  it("показывает текущий диапазон и переходит вперед", () => {
    const handleOffsetChange = vi.fn();

    render(
      <TablePagination
        limit={1}
        offset={0}
        total={2}
        isLoading={false}
        onOffsetChange={handleOffsetChange}
      />,
    );

    expect(screen.getByText("Показано 1-1 из 2")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Вперёд" }));

    expect(handleOffsetChange).toHaveBeenCalledWith(1);
  });

  it("скрывается, если все записи помещаются на одну страницу", () => {
    const { container } = render(
      <TablePagination
        limit={10}
        offset={0}
        total={2}
        isLoading={false}
        onOffsetChange={vi.fn()}
      />,
    );

    expect(container).toBeEmptyDOMElement();
  });
});
