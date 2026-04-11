# Frontend

## Переменные окружения

Для локальной разработки фронтенд использует файл `.env.dev`.

Обязательные переменные:

- `NEXT_PUBLIC_API_URL` — базовый URL backend API.

## Docker

Для разработки используется `Dockerfile.dev` и `npm run dev`.

Production-сборка использует `Dockerfile` и ожидает `NEXT_PUBLIC_API_URL` через `--build-arg`.

Пример production-сборки:

```bash
docker build \
  -f frontend/Dockerfile \
  --build-arg NEXT_PUBLIC_API_URL=https://api.example.com \
  -t frontend-prod \
  ./frontend
```
