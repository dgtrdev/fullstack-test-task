"use client";

import { FormEvent, useEffect, useState } from "react";
import {
  Alert,
  Button,
  Card,
  Col,
  Container,
  Row,
} from "react-bootstrap";
import { AlertsTable } from "../components/alerts-table";
import { FilesTable } from "../components/files-table";
import { UploadFileModal } from "../components/upload-file-modal";
import { fetchAlerts } from "../shared/api/alerts";
import { fetchFiles, uploadFile } from "../shared/api/files";
import type { AlertItem } from "../shared/types/alerts";
import type { FileItem } from "../shared/types/files";


export default function Page() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [filesTotal, setFilesTotal] = useState(0);
  const [alertsTotal, setAlertsTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function loadData() {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const [filesData, alertsData] = await Promise.all([
        fetchFiles(),
        fetchAlerts(),
      ]);

      setFiles(filesData.items);
      setFilesTotal(filesData.total);
      setAlerts(alertsData.items);
      setAlertsTotal(alertsData.total);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Произошла ошибка");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadData();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!title.trim() || !selectedFile) {
      setErrorMessage("Укажите название и выберите файл");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      await uploadFile(title.trim(), selectedFile);
      setShowModal(false);
      setTitle("");
      setSelectedFile(null);
      await loadData();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Произошла ошибка");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Container fluid className="py-4 px-4 bg-light min-vh-100">
      <Row className="justify-content-center">
        <Col xxl={10} xl={11}>
          <Card className="shadow-sm border-0 mb-4">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start gap-3 flex-wrap">
                <div>
                  <h1 className="h3 mb-2">Управление файлами</h1>
                  <p className="text-secondary mb-0">
                    Загрузка файлов, просмотр статусов обработки и ленты алертов.
                  </p>
                </div>
                <div className="d-flex gap-2">
                  <Button variant="outline-secondary" onClick={() => void loadData()}>
                    Обновить
                  </Button>
                  <Button variant="primary" onClick={() => setShowModal(true)}>
                    Добавить файл
                  </Button>
                </div>
              </div>
            </Card.Body>
          </Card>

          {errorMessage ? (
            <Alert variant="danger" className="shadow-sm">
              {errorMessage}
            </Alert>
          ) : null}

          <FilesTable files={files} total={filesTotal} isLoading={isLoading} />
          <AlertsTable alerts={alerts} total={alertsTotal} isLoading={isLoading} />
        </Col>
      </Row>

      <UploadFileModal
        isSubmitting={isSubmitting}
        show={showModal}
        title={title}
        onHide={() => setShowModal(false)}
        onSelectedFileChange={setSelectedFile}
        onSubmit={handleSubmit}
        onTitleChange={setTitle}
      />
    </Container>
  );
}
