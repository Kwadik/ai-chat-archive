# Local HTTP API

Локальный HTTP API для работы с архивом AI Chat.

Сервер работает только локально и использует файловое хранилище как источник истины.

## Base URL

По умолчанию сервер слушает:

```text
http://127.0.0.1:<port>
```

---

## Projects

### GET /projects

Возвращает список проектов.

#### Response

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

### POST /projects

Создаёт проект.

#### Request

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

#### Response

`201 Created`

```json
{
  "id": "my-project",
  "name": "My Project"
}
```

При некорректном JSON или отсутствии обязательных полей:

`400 Bad Request`

---

### GET /projects/{project_id}

Возвращает один проект.

#### Response

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

## Chats

### GET /projects/{project_id}/chats

Возвращает список чатов проекта.

#### Response

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

### POST /projects/{project_id}/chats

Создаёт чат в проекте.

#### Request

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

#### Response

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

При некорректном JSON или отсутствии обязательных полей:

`400 Bad Request`

---

### GET /projects/{project_id}/chats/{provider}/{chat_id}

Возвращает чат вместе с его сообщениями.

#### Response

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

## Messages

### POST /projects/{project_id}/chats/{provider}/{chat_id}/messages

Добавляет сообщение в существующий чат.

Номер сообщения назначается сервером автоматически.

#### Request

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

#### Response

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

При некорректном JSON или отсутствии обязательных полей:

`400 Bad Request`

---

## Error responses

Текущая реализация использует стандартные HTTP error responses Python `http.server`.

Основные коды:

| Status | Значение            |
| ------ | ------------------- |
| `200`  | Успешный GET        |
| `201`  | Ресурс создан       |
| `400`  | Некорректный запрос |
| `404`  | Ресурс не найден    |

Формат тела ошибок пока **не является частью API-контракта**.

---

## Current API scope

На текущем этапе API намеренно минимален.

Поддерживаются:

* создание и чтение проектов;
* создание и чтение чатов;
* добавление сообщений;
* получение полного чата с Markdown-содержимым сообщений.

Пока не реализованы:

* обновление проектов;
* обновление чатов;
* редактирование сообщений;
* удаление ресурсов;
* поиск;
* пагинация;
* авторизация;
* удалённый доступ.

Эти возможности будут добавляться только при появлении соответствующего требования.

