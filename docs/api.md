# Local HTTP API

Локальный HTTP API для работы с архивом AI Chat Archive.

API работает только локально и использует файловое хранилище как источник истины.

Основные потребители:

* browser extension;
* Python API client;
* локальные инструменты в будущем.

API не имеет собственного хранилища данных.

---

## Base URL

По умолчанию сервер слушает:

```text
http://127.0.0.1:<port>
```

Конкретный порт задаётся при запуске сервера.

API рассчитан на локальное использование и не предоставляет:

* удалённый доступ;
* авторизацию;
* cloud storage;
* multi-user access.

---

# Projects

## GET /projects

Возвращает список проектов.

### Response

`200 OK`

```json
[
  {
    "id": "my-project",
    "name": "My Project"
  }
]
```

Если проектов нет:

```json
[]
```

---

## POST /projects

Создаёт проект.

### Request

```json
{
  "id": "my-project",
  "name": "My Project",
  "description": "Project description",
  "root_path": "E:\\Projects\\my-project"
}
```

Обязательные поля:

* `id`
* `name`

Необязательные поля:

* `description`
* `root_path`

### Response

`201 Created`

```json
{
  "id": "my-project",
  "name": "My Project"
}
```

`description` и `root_path` принимаются сервером, но не возвращаются в ответе создания.

При некорректном JSON, отсутствии обязательного поля или неправильном типе:

`400 Bad Request`

---

## GET /projects/{project_id}

Возвращает один проект.

### Response

`200 OK`

```json
{
  "id": "my-project",
  "name": "My Project",
  "description": "Project description",
  "root_path": "E:\\Projects\\my-project"
}
```

Если проект не существует:

`404 Not Found`

---

# Chats

## GET /projects/{project_id}/chats

Возвращает список чатов проекта.

### Response

`200 OK`

```json
[
  {
    "id": "chat-123",
    "provider": "chatgpt",
    "title": "Working on API",
    "project_id": "my-project"
  }
]
```

Если чатов нет:

```json
[]
```

Если проект не существует:

`404 Not Found`

---

## POST /projects/{project_id}/chats

Создаёт чат в проекте.

### Request

```json
{
  "id": "chat-123",
  "provider": "chatgpt",
  "title": "Working on API",
  "metadata": {
    "url": "https://chatgpt.com/c/chat-123",
    "source": "manual"
  }
}
```

Обязательные поля:

* `id`
* `provider`
* `title`

Необязательное поле:

* `metadata`

### Response

`201 Created`

```json
{
  "id": "chat-123",
  "provider": "chatgpt",
  "title": "Working on API"
}
```

Если проект не существует:

`404 Not Found`

При некорректном JSON, отсутствии обязательного поля или неправильном типе:

`400 Bad Request`

---

## GET /projects/{project_id}/chats/{provider}/{chat_id}

Возвращает чат вместе со всеми его сообщениями.

### Response

`200 OK`

```json
{
  "id": "chat-123",
  "provider": "chatgpt",
  "title": "Working on API",
  "project_id": "my-project",
  "metadata": {
    "url": "https://chatgpt.com/c/chat-123",
    "source": "manual"
  },
  "messages": [
    {
      "number": 1,
      "role": "user",
      "content": "# Hello\n\nWorld",
      "file_name": "001-user.md"
    },
    {
      "number": 2,
      "role": "assistant",
      "content": "Привет!",
      "file_name": "002-assistant.md"
    }
  ]
}
```

Metadata сообщений в текущем GET-ответе **не возвращается**.

Если чат существует, но сообщений нет:

```json
{
  "id": "chat-123",
  "provider": "chatgpt",
  "title": "Empty Chat",
  "project_id": "my-project",
  "metadata": {},
  "messages": []
}
```

Если чат не существует:

`404 Not Found`

---

# Messages

## POST /projects/{project_id}/chats/{provider}/{chat_id}/messages

Добавляет сообщение в существующий чат.

Номер сообщения назначается сервером автоматически.

### Request

```json
{
  "role": "user",
  "content": "# Hello\n\nWorld",
  "metadata": {
    "source": "manual-copy",
    "format": "markdown"
  }
}
```

Обязательные поля:

* `role`
* `content`

Необязательное поле:

* `metadata`

### Response

`201 Created`

```json
{
  "number": 1,
  "role": "user",
  "file_name": "001-user.md"
}
```

Следующее сообщение получает следующий номер:

```json
{
  "number": 2,
  "role": "assistant",
  "file_name": "002-assistant.md"
}
```

Если чат не существует:

`404 Not Found`

При некорректном JSON, отсутствии обязательного поля или неправильном типе:

`400 Bad Request`

---

## PUT /projects/{project_id}/chats/{provider}/{chat_id}/messages/{number}

Редактирует существующее сообщение.

Сообщение идентифицируется комбинацией:

```text
project_id
provider
chat_id
number
```

Отдельный `message_id` API не использует.

### Request

```json
{
  "role": "assistant",
  "content": "Edited Markdown content",
  "metadata": {
    "source": "manual-copy",
    "edited": true
  }
}
```

Обязательные поля:

* `role`
* `content`

Необязательное поле:

* `metadata`

Если `metadata` не передан, сохраняется существующее значение metadata сообщения.

### Response

`200 OK`

```json
{
  "number": 2,
  "role": "assistant",
  "file_name": "002-assistant.md",
  "metadata": {
    "source": "manual-copy",
    "edited": true
  }
}
```

При обновлении:

* номер сообщения сохраняется;
* существующий `file_name` сохраняется;
* `created_at` сохраняется;
* `updated_at` обновляется при изменении;
* новое сообщение не создаётся.

Если проект не существует:

`404 Not Found`

Если чат не существует:

`404 Not Found`

Если сообщение с указанным номером не существует:

`404 Not Found`

Если номер сообщения не является целым числом:

`404 Not Found`

При некорректном JSON, отсутствии обязательного поля или неправильном типе:

`400 Bad Request`

---

# Search

## GET /search

Выполняет поиск по содержимому сообщений.

Поиск выполняется через файловое хранилище.

### Query parameters

Поддерживаются:

| Parameter    | Обязательный | Описание                         |
| ------------ | ------------ | -------------------------------- |
| `q`          | нет          | Текст поиска                     |
| `project_id` | нет          | Ограничить поиск проектом        |
| `chat_id`    | нет          | Ограничить поиск чатом           |
| `role`       | нет          | Ограничить поиск ролью сообщения |

Пример:

```text
GET /search?q=python
```

С фильтром проекта:

```text
GET /search?q=python&project_id=my-project
```

С фильтром чата:

```text
GET /search?q=python&chat_id=chat-123
```

С фильтром роли:

```text
GET /search?q=python&role=assistant
```

Параметры могут комбинироваться:

```text
GET /search?q=python&project_id=my-project&role=assistant
```

`provider` не является отдельным параметром фильтра.

Provider возвращается как часть контекста результата.

### Пустой запрос

Если `q` не указан или пустой, поиск по тексту не ограничивается содержимым.

Например:

```text
GET /search
```

возвращает сообщения, удовлетворяющие остальным переданным фильтрам.

Если одновременно не задан ни текст поиска, ни какой-либо фильтр, результатом является пустой список.

### Response

`200 OK`

```json
[
  {
    "project": {
      "id": "my-project",
      "name": "My Project"
    },
    "chat": {
      "id": "chat-123",
      "provider": "chatgpt",
      "title": "Working on API",
      "project_id": "my-project"
    },
    "message": {
      "number": 2,
      "role": "assistant",
      "content": "Working with Python...",
      "file_name": "002-assistant.md"
    },
    "provider": "chatgpt"
  }
]
```

Если ничего не найдено:

```json
[]
```

Поиск по содержимому является регистронезависимым.

Поиск выполняется непосредственно по файловому архиву. Отдельный поисковый индекс не используется.

---

# Content Encoding

JSON responses используют:

```text
Content-Type: application/json
```

JSON сериализуется с сохранением Unicode-символов.

Markdown content передаётся как обычная JSON-строка.

Например:

```json
{
  "content": "# Привет\n\nТекст сообщения"
}
```

API не преобразует Markdown в HTML.

HTML является ответственностью viewer/presentation layer.

---

# Metadata

Project, Chat и Message могут иметь metadata на уровне domain/storage.

В текущем HTTP API:

* Project metadata отдельно не передаётся;
* Chat metadata возвращается при `GET /projects/{project_id}/chats/{provider}/{chat_id}`;
* Message metadata принимается при создании;
* Message metadata возвращается при обновлении через `PUT`.

Пример Chat metadata:

```json
{
  "metadata": {
    "url": "https://chatgpt.com/c/chat-123",
    "source": "manual"
  }
}
```

Пример Message metadata:

```json
{
  "metadata": {
    "source": "manual-copy",
    "format": "markdown"
  }
}
```

Metadata предназначена для структурированной информации и интеграций.

Она не заменяет Markdown content.

---

# Error Responses

Текущая реализация использует стандартные HTTP error responses Python `http.server`.

Основные коды:

| Status | Значение            |
| ------ | ------------------- |
| `200`  | Успешный запрос     |
| `201`  | Ресурс создан       |
| `400`  | Некорректный запрос |
| `404`  | Ресурс не найден    |

Тело ошибки сейчас формируется через стандартный `send_error()`.

Формат тела ошибок **не является стабильной частью API-контракта**.

Клиенты не должны зависеть от текста error response.

---

# Current API Scope

На текущем этапе реализованы:

### Projects

* `GET /projects`
* `POST /projects`
* `GET /projects/{project_id}`

### Chats

* `GET /projects/{project_id}/chats`
* `POST /projects/{project_id}/chats`
* `GET /projects/{project_id}/chats/{provider}/{chat_id}`

### Messages

* `POST /projects/{project_id}/chats/{provider}/{chat_id}/messages`
* `PUT /projects/{project_id}/chats/{provider}/{chat_id}/messages/{number}`

### Search

* `GET /search`

---

# Not Implemented

В текущем HTTP API отсутствуют:

* обновление проектов;
* обновление чатов;
* удаление проектов;
* удаление чатов;
* удаление сообщений;
* пагинация;
* авторизация;
* удалённый доступ;
* отдельный search index;
* background synchronization.

Эти возможности добавляются только при появлении соответствующего use case.

---

# Typical Extension Flow

Основной сценарий browser extension:

```text
ChatGPT
   │
   │ user copies Markdown
   ▼
Browser Extension
   │
   │ user edits Markdown
   ▼
ExtensionApiClient
   │
   │ POST /projects/.../messages
   ▼
Local HTTP API
   │
   ▼
FileStorage
   │
   ▼
Markdown file
```

Для редактирования уже сохранённого сообщения:

```text
Browser Extension
   │
   │ PUT /projects/.../messages/<number>
   ▼
Local HTTP API
   │
   ▼
FileStorage.save_message()
   │
   ▼
existing Markdown file
```

Extension не работает напрямую с filesystem layout.

Он использует HTTP API.

---

# API Design Principles

## Local only

API предназначен для локального использования.

## Filesystem as source of truth

HTTP API не создаёт отдельную базу данных.

Все изменения проходят через `FileStorage`.

## Markdown as source of truth

API передаёт Markdown без преобразования в HTML.

## Natural message addressing

Message адресуется через:

```text
project_id
+ provider
+ chat_id
+ number
```

## Thin HTTP layer

HTTP handler отвечает за:

* parsing request;
* basic validation;
* вызов storage/application logic;
* формирование HTTP response.

Filesystem behavior не должен дублироваться в HTTP handler.

## Provider independent

HTTP API не должен знать, как конкретный provider определяет:

* chat ID;
* chat title;
* URL;
* DOM structure;
* clipboard content.

Эта логика принадлежит browser extension provider adapter.

## Minimal surface

Новые endpoint'ы добавляются только при наличии реального требования.
