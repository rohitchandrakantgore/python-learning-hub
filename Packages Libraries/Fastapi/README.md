# FastAPI Learning App

This folder contains a small FastAPI application demonstrating path and query
parameters, request-body validation with Pydantic, and automatically generated
API documentation.

## Application

`main.py` creates the FastAPI app and defines an `Item` request model:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, item_name: str | None = None):
    return {"item_id": item_id, "item_name": item_name}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}
```

FastAPI uses Python type annotations to validate and convert request data.
`Item` is a Pydantic model: `name` and `price` are required, while
`is_offer` is optional and defaults to `null`.

## Python type hints

Type hints describe the values a function accepts and returns. Python does not
enforce annotations by itself, but FastAPI uses them to parse and validate
request data and to generate API documentation.

### Basic types

Common annotations include `str`, `int`, `float`, `bool`, and `bytes`:

```python
def get_full_name(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name}"


def describe_age(name: str, age: int) -> str:
    return f"{name} is {age} years old"
```

### Collection types

Use built-in collection types with an element type (Python 3.9+):

```python
from typing import Any


def get_names(names: list[str]) -> list[str]:
    return names


def get_scores(scores: dict[str, float]) -> dict[str, float]:
    return scores
```

Other common forms include `set[int]`, `tuple[str, int]`, and
`list[Any]`. Use `Any` from `typing` only when values can genuinely be of any
type; it provides less useful validation and editor support.

### Union and optional types

A union allows a value to have more than one type. Use `|` syntax with Python
3.10 and later:

```python
def get_name_or_id(value: str | int) -> str | int:
    return value


def greet(name: str | None = None) -> str:
    if name is None:
        return "Hello, Stranger!"
    return f"Hello, {name}!"
```

`str | None` means a value can be a string or `None`. When using Python 3.9 or
earlier, write `Union[str, int]` and `Optional[str]` from the `typing` module.

### Classes as types

Classes can be used as annotations for function parameters and return values:

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


def get_person_info(person: Person) -> str:
    return f"{person.name} is {person.age} years old"
```

### Pydantic models

Pydantic models define and validate structured data. FastAPI commonly uses
them to describe JSON request bodies:

```python
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: str | None = None
    friends: list[int] = []


user = User(id="123", friends=[1, 2, 3])
print(user.id)  # 123 (parsed as an integer)
```

For production models with mutable defaults, prefer a `default_factory`:

```python
from pydantic import BaseModel, Field


class User(BaseModel):
    friends: list[int] = Field(default_factory=list)
```

## Install and run

From the repository root, install the project dependencies and start the
development server from this folder:

```bash
python -m pip install -r requirements.txt
cd "Packages Libraries/Fastapi"
python -m uvicorn main:app --reload
```

The server runs at <http://127.0.0.1:8000>. `--reload` restarts it when source
files change; use it for local development, not production.

## API

| Method | Path | Inputs | Successful response |
| --- | --- | --- | --- |
| `GET` | `/` | None | `200` with `{"Hello": "World"}` |
| `GET` | `/items/{item_id}` | Integer path parameter `item_id`; optional string query parameter `item_name` | `200` with the supplied values |
| `PUT` | `/items/{item_id}` | Integer path parameter `item_id`; JSON `Item` body | `200` with the ID and validated item |

### Example requests

Retrieve an item, with an optional query parameter:

```bash
curl "http://127.0.0.1:8000/items/42?item_name=notebook"
```

```json
{
  "item_id": 42,
  "item_name": "notebook"
}
```

Update an item by sending a JSON body:

```bash
curl -X PUT "http://127.0.0.1:8000/items/42" \
  -H "Content-Type: application/json" \
  -d '{"name":"Notebook","price":4.5,"is_offer":true}'
```

The response contains the path ID and the item data:

```json
{
  "item_id": 42,
  "item": {
    "name": "Notebook",
    "price": 4.5,
    "is_offer": true
  }
}
```

Invalid path, query, or body values are rejected with a `422 Unprocessable
Entity` response and validation details. For example, `item_id` must be an
integer, and the request body must include `name` and `price`.

## Interactive API documentation

While the server is running, open:

- <http://127.0.0.1:8000/docs> for Swagger UI
- <http://127.0.0.1:8000/redoc> for ReDoc
- <http://127.0.0.1:8000/openapi.json> for the generated OpenAPI schema

The documentation pages let you inspect the routes and send requests directly
from the browser.
