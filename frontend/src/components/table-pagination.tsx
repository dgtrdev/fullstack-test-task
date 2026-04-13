import { Button } from "react-bootstrap";


type TablePaginationProps = {
  limit: number;
  offset: number;
  total: number;
  isLoading: boolean;
  onOffsetChange: (offset: number) => void;
};


export function TablePagination({
  limit,
  offset,
  total,
  isLoading,
  onOffsetChange,
}: TablePaginationProps) {
  if (total <= limit) {
    return null;
  }

  const pageStart = total === 0 ? 0 : offset + 1;
  const pageEnd = Math.min(offset + limit, total);
  const previousOffset = Math.max(offset - limit, 0);
  const nextOffset = offset + limit;
  const canGoBack = offset > 0;
  const canGoForward = nextOffset < total;

  return (
    <div className="d-flex justify-content-between align-items-center gap-3 flex-wrap mt-3">
      <span className="text-secondary small">
        Показано {pageStart}-{pageEnd} из {total}
      </span>
      <div className="d-flex gap-2">
        <Button
          variant="outline-secondary"
          size="sm"
          disabled={!canGoBack || isLoading}
          onClick={() => onOffsetChange(previousOffset)}
        >
          Назад
        </Button>
        <Button
          variant="outline-secondary"
          size="sm"
          disabled={!canGoForward || isLoading}
          onClick={() => onOffsetChange(nextOffset)}
        >
          Вперёд
        </Button>
      </div>
    </div>
  );
}
