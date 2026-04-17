import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import type { FileItem } from "../shared/types/files";
import { FilesTable } from "./files-table";


const baseFile: FileItem = {
  id: "file-1",
  title: "Документ",
  original_name: "document.txt",
  mime_type: "text/plain",
  size: 128,
  processing_status: "processed",
  scan_status: "clean",
  scan_details: "no threats found",
  metadata_json: null,
  requires_attention: false,
  created_at: "2026-04-13T10:00:00Z",
  updated_at: "2026-04-13T10:00:00Z",
  deleted_at: null,
};

function renderFilesTable(files: FileItem[]) {
  return render(
    <FilesTable
      errorMessage={null}
      files={files}
      isLoading={false}
      limit={10}
      offset={0}
      total={files.length}
      onOffsetChange={vi.fn()}
    />,
  );
}


describe("FilesTable", () => {
  it("не показывает лишние детали для clean-статуса", () => {
    renderFilesTable([baseFile]);

    expect(screen.getByText("clean")).toBeInTheDocument();
    expect(screen.queryByText("no threats found")).not.toBeInTheDocument();
  });

  it("не показывает подпись для pending-статуса", () => {
    renderFilesTable([
      {
        ...baseFile,
        scan_status: null,
        scan_details: null,
      },
    ]);

    expect(screen.getByText("pending")).toBeInTheDocument();
    expect(screen.queryByText("Ожидает обработки")).not.toBeInTheDocument();
  });

  it("показывает детали для suspicious-статуса", () => {
    renderFilesTable([
      {
        ...baseFile,
        scan_status: "suspicious",
        scan_details: "suspicious extension .js",
        requires_attention: true,
      },
    ]);

    expect(screen.getByText("suspicious")).toBeInTheDocument();
    expect(screen.getByText("suspicious extension .js")).toBeInTheDocument();
  });
});
