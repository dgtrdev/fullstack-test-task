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
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 \
  -t fullstack-frontend-prod \
  ./frontend
```

Запуск собранного production-образа:

```bash
docker run --rm \
  -p 3000:3000 \
  fullstack-frontend-prod
```
