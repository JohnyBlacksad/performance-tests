# Performance Tests

Проект для проведения нагрузочного тестирования с использованием Locust. Предоставляет инфраструктуру для тестирования API через HTTP и gRPC протоколы.

## Оглавление

- [Описание](#описание)
- [Структура проекта](#структура-проекта)
- [Сценарии тестирования](#сценарии-тестирования)
- [Установка](#установка)
- [Конфигурация](#конфигурация)
- [Запуск тестов](#запуск-тестов)
  - [Локальный запуск](#локальный-запуск)
  - [Запуск с HTML-отчётом](#запуск-с-html-отчётом)
- [Генерация тестовых данных (Seeds)](#генерация-тестовых-данных-seeds)
  - [Запуск генерации](#запуск-генерации)
  - [Загрузка сохранённых данных](#загрузка-сохранённых-данных)
- [Зависимости](#зависимости)
- [CI/CD](#cicd)
- [Лицензия](#лицензия)

## Описание

Проект представляет собой набор сценариев нагрузочного тестирования для финансовой системы. Поддерживает тестирование через:

- HTTP API (REST)
- gRPC

Тестовый стенд: [Performance QA Engineer Course](https://github.com/Nikita-Filonov/performance-qa-engineer-course)

## Структура проекта

```
performance-tests/
├── clients/              # HTTP и gRPC клиенты для взаимодействия с API
│   ├── grpc/            # gRPC клиенты для различных сервисов
│   └── http/            # HTTP клиенты для различных сервисов
├── contracts/           # Protobuf контракты (pb2 файлы)
├── scenarios/           # Сценарии нагрузочного тестирования
│   ├── grpc/           # gRPC сценарии
│   └── http/           # HTTP сценарии
├── seeds/              # Сиды данных для тестирования
│   ├── scenarios/      # Реализации сценариев генерации
│   ├── schema/         # Pydantic схемы для планов и результатов
│   ├── builder.py      # SeedsBuilder для генерации данных
│   └── dumps.py        # Утилиты сохранения/загрузки
├── tools/              # Утилиты и вспомогательные модули
│   ├── config/         # Конфигурация через pydantic-settings
│   ├── locust/         # Базовые классы для Locust
│   ├── fakers.py       # Генераторы тестовых данных
│   └── logger.py       # Логирование
├── config.py           # Основная конфигурация приложения
├── main.py             # Точка входа
├── requirements.txt    # Зависимости Python
└── .env                # Переменные окружения
```

## Сценарии тестирования

### gRPC сценарии

- `existing_user_get_documents` — получение документов существующего пользователя
- `existing_user_get_operations` — получение операций существующего пользователя
- `existing_user_issue_virtual_card` — выпуск виртуальной карты
- `existing_user_make_purchase_operation` — операция покупки
- `new_user_get_accounts` — получение счетов нового пользователя
- `new_user_get_documents` — получение документов нового пользователя
- `new_user_issue_physical_card` — выпуск физической карты
- `new_user_make_top_up_operation` — операция пополнения счёта

### HTTP сценарии

Аналогичные gRPC сценарии, но через HTTP API:

- `existing_user_get_documents`
- `existing_user_get_operations`
- `existing_user_issue_virtual_card`
- `existing_user_make_purchase_operation`
- `new_user_get_accounts`
- `new_user_get_documents`
- `new_user_issue_physical_card`
- `new_user_make_top_up_operation`

## Установка

### Требования

- Python 3.12+
- Docker и Docker Compose (для запуска тестовых сервисов)

### Установка зависимостей

**Linux/macOS:**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Windows (cmd):**

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Конфигурация

Конфигурация осуществляется через файл `.env`:

```env
LOCUST_USER.MIN_WAIT=1
LOCUST_USER.MAX_WAIT=3

GATEWAY_HTTP_CLIENT.URL=http://localhost:8003
GATEWAY_HTTP_CLIENT.API_VERSION=1
GATEWAY_HTTP_CLIENT.TIMEOUT=100

GATEWAY_GRPC_CLIENT.HOST=localhost
GATEWAY_GRPC_CLIENT.PORT=9003
```

Параметры:

- `LOCUST_USER.MIN_WAIT` — минимальное время ожидания между задачами (секунды)
- `LOCUST_USER.MAX_WAIT` — максимальное время ожидания между задачами (секунды)
- `GATEWAY_HTTP_CLIENT.URL` — URL HTTP API
- `GATEWAY_HTTP_CLIENT.API_VERSION` — версия API
- `GATEWAY_HTTP_CLIENT.TIMEOUT` — таймаут запросов (секунды)
- `GATEWAY_GRPC_CLIENT.HOST` — хост gRPC сервера
- `GATEWAY_GRPC_CLIENT.PORT` — порт gRPC сервера

## Запуск тестов

### Локальный запуск

**Linux/macOS:**

```bash
# Запуск сценария HTTP
locust --config=./scenarios/http/gateway/new_user_get_accounts/v1.0.conf --host=http://localhost:8003

# Запуск сценария gRPC
locust --config=./scenarios/grpc/gateway/new_user_get_accounts/v1.0.conf
```

**Windows (PowerShell):**

```powershell
# Запуск сценария HTTP
locust --config=./scenarios/http/gateway/new_user_get_accounts/v1.0.conf --host=http://localhost:8003

# Запуск сценария gRPC
locust --config=./scenarios/grpc/gateway/new_user_get_accounts/v1.0.conf
```

**Windows (cmd):**

```cmd
REM Запуск сценария HTTP
locust --config=./scenarios/http/gateway/new_user_get_accounts/v1.0.conf --host=http://localhost:8003

REM Запуск сценария gRPC
locust --config=./scenarios/grpc/gateway/new_user_get_accounts/v1.0.conf
```

### Запуск с HTML-отчётом

**Linux/macOS:**

```bash
locust --config=./scenarios/http/gateway/new_user_get_accounts/v1.0.conf --html=./reports/index.html
```

**Windows (PowerShell):**

```powershell
locust --config=./scenarios/http/gateway/new_user_get_accounts/v1.0.conf --html=./reports/index.html
```

**Windows (cmd):**

```cmd
locust --config=./scenarios/http/gateway/new_user_get_accounts/v1.0.conf --html=./reports/index.html
```

## Генерация тестовых данных (Seeds)

Модуль `seeds` предназначен для предварительной генерации тестовых данных (пользователи, счета, карты, операции) перед запуском нагрузочных тестов.

### Архитектура

- **SeedsBuilder** — основной класс для генерации данных через gRPC или HTTP клиенты
- **SeedsPlan** — план генерации (количество пользователей, счетов, карт, операций)
- **SeedsResult** — результат генерации с идентификаторами созданных объектов
- **SeedsScenario** — базовый класс для сценариев генерации

### Запуск генерации

**Linux/macOS:**

```bash
# Генерация данных для сценария existing_user_get_documents
python -c "from seeds.scenarios.existing_user_get_documents import ExistingUserGetDocumentsScenario; ExistingUserGetDocumentsScenario().build()"
```

**Windows (PowerShell):**

```powershell
python -c "from seeds.scenarios.existing_user_get_documents import ExistingUserGetDocumentsScenario; ExistingUserGetDocumentsScenario().build()"
```

**Windows (cmd):**

```cmd
python -c "from seeds.scenarios.existing_user_get_documents import ExistingUserGetDocumentsScenario; ExistingUserGetDocumentsScenario().build()"
```

### Доступные сценарии генерации

- `existing_user_get_documents` — данные для теста получения документов
- `existing_user_get_operations` — данные для теста получения операций
- `existing_user_issue_virtual_card` — данные для теста выпуска виртуальной карты
- `existing_user_make_purchase_operation` — данные для теста операции покупки

### Сохранение и загрузка данных

Результаты генерации сохраняются в директорию `dumps/` в формате JSON:

```bash
# Файл будет сохранён как dumps/{scenario}_seeds.json
```

**Загрузка сохранённых данных:**

```python
from seeds.dumps import load_seeds_results

# Загрузка данных для сценария
result = load_seeds_results('existing_user_get_documents')
```

### Программное использование SeedsBuilder

```python
from seeds.builder import build_grpc_seeds_builder
from seeds.schema.plan import SeedsPlan, SeedUsersPlan

# Создать builder с gRPC клиентами
builder = build_grpc_seeds_builder()

# Создать план генерации (10 пользователей)
plan = SeedsPlan(users=SeedUsersPlan(count=10))

# Сгенерировать данные
result = builder.build(plan)

# Результат содержит идентификаторы всех созданных объектов
print(f"Создано пользователей: {len(result.users)}")
```

## Зависимости

- `locust` — фреймворк для нагрузочного тестирования
- `grpcio`, `grpcio-tools` — работа с gRPC
- `httpx` — HTTP клиент
- `pydantic`, `pydantic-settings` — валидация и конфигурация
- `Faker` — генерация тестовых данных

## CI/CD

Проект использует GitHub Actions для автоматизации запуска тестов. Воркфлоу настроено на ручной запуск через `workflow_dispatch` с выбором сценария.

Для запуска перейдите на вкладку Actions в репозитории, выберите workflow "Performance Tests" и нажмите "Run workflow".

После завершения теста HTML-отчёт автоматически публикуется на GitHub Pages.

## Лицензия

Проект для курса по нагрузочному тестированию.
