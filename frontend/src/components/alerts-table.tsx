import { Alert, Badge, Card, Spinner, Table } from "react-bootstrap";

import { getLevelVariant } from "../shared/lib/badges";
import { formatDate } from "../shared/lib/format";
import type { AlertItem } from "../shared/types/alerts";


type AlertsTableProps = {
  alerts: AlertItem[];
  errorMessage: string | null;
  total: number;
  isLoading: boolean;
};


export function AlertsTable({ alerts, errorMessage, total, isLoading }: AlertsTableProps) {
  return (
    <Card className="shadow-sm border-0">
      <Card.Header className="bg-white border-0 pt-4 px-4">
        <div className="d-flex justify-content-between align-items-center">
          <h2 className="h5 mb-0">Алерты</h2>
          <Badge bg="secondary">{total}</Badge>
        </div>
      </Card.Header>
      <Card.Body className="px-4 pb-4">
        {errorMessage ? (
          <Alert variant="danger" className="mb-0">
            {errorMessage}
          </Alert>
        ) : isLoading ? (
          <div className="d-flex justify-content-center py-5">
            <Spinner animation="border" />
          </div>
        ) : (
          <div className="table-responsive">
            <Table hover bordered className="align-middle mb-0">
              <thead className="table-light">
                <tr>
                  <th>ID</th>
                  <th>File ID</th>
                  <th>Уровень</th>
                  <th>Сообщение</th>
                  <th>Создан</th>
                </tr>
              </thead>
              <tbody>
                {alerts.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="text-center py-4 text-secondary">
                      Алертов пока нет
                    </td>
                  </tr>
                ) : (
                  alerts.map((item) => (
                    <tr key={item.id}>
                      <td>{item.id}</td>
                      <td className="small">{item.file_id}</td>
                      <td>
                        <Badge bg={getLevelVariant(item.level)}>{item.level}</Badge>
                      </td>
                      <td>{item.message}</td>
                      <td>{formatDate(item.created_at)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </Table>
          </div>
        )}
      </Card.Body>
    </Card>
  );
}
