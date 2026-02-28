# py-api-builder

A Python code generator that creates Flask API wrappers around external REST APIs. Define your endpoints once, and `py-api-builder` generates a complete Flask application that proxies requests to an upstream service.

## Features

- Generate Flask apps from a simple Python API
- Support for GET and POST HTTP methods
- JSON and typed (e.g. `str`, `int`) response handling
- Inject custom code into generated endpoint bodies
- Output generated code as a string or write it directly to a file

## Requirements

- Python >= 3.14
- `flask` and `requests` (in the **generated** code, not needed to run the builder itself)

## Installation

Clone the repository:

```bash
git clone <repo-url>
cd py_package_builder
```

## Quick Start

```python
from main import APIBuilder

# Create a builder targeting an external API
builder = APIBuilder("my_api", "https://jsonplaceholder.typicode.com/posts")

# Add a GET endpoint that returns JSON
builder.add_endpoint("get_posts", "json", "get")

# Print the generated Flask application code
print(builder.get_code())
```

This outputs a complete Flask application you can save and run.

## Examples

### 1. Basic JSON Endpoint

The simplest case — proxy a single JSON API:

```python
from main import APIBuilder

builder = APIBuilder("jsonplaceholder", "https://jsonplaceholder.typicode.com/posts")
builder.add_endpoint("get_posts", "json", "get")

print(builder.get_code())
```

**Generated output:**

```python
from flask import Flask
import requests
from json import loads
from typing import TypeAlias

app: Flask = Flask(__name__)

def get_posts() -> ...:

    return (requests.get('https://jsonplaceholder.typicode.com/posts').json)
```

### 2. Multiple Endpoints

Build a full API proxy with several routes:

```python
from main import APIBuilder

builder = APIBuilder("blog_api", "https://jsonplaceholder.typicode.com")

# GET endpoints
builder.add_endpoint("get_posts", "json", "get")
builder.add_endpoint("get_comments", "json", "get")
builder.add_endpoint("get_users", "json", "get")

# POST endpoint
builder.add_endpoint("create_post", "json", "post")

print(builder.get_code())
```

### 3. Non-JSON (String) Responses

When the upstream API returns plain text or HTML instead of JSON, pass a
Python type like `str` to cast the response:

```python
from main import APIBuilder

builder = APIBuilder("html_fetcher", "https://httpbin.org/html")

# Returns raw HTML as a str
builder.add_endpoint("fetch_html", str, "get")

print(builder.get_code())
```

**Generated output:**

```python
def fetch_html() -> <class 'str'>:

    return <class 'str'>(requests.get('https://httpbin.org/html').text)
```

### 4. Injecting Extra Code

Use the `extra_code` parameter to add logging, validation, or setup logic
that runs before the API request:

```python
from main import APIBuilder

builder = APIBuilder("debug_api", "https://jsonplaceholder.typicode.com/posts")

# Add a debug print statement
builder.add_endpoint(
    name="get_posts_debug",
    returntype="json",
    api_type="get",
    extra_code='print("Fetching posts...")',
)

# Add a logging call
builder.add_endpoint(
    name="get_posts_logged",
    returntype="json",
    api_type="get",
    extra_code='import logging; logging.info("GET /posts called")',
)

print(builder.get_code())
```

### 5. Writing Generated Code to a File

A complete end-to-end workflow:

```python
from main import APIBuilder

builder = APIBuilder("my_api", "https://api.example.com/v1/data")

builder.add_endpoint("list_items", "json", "get")
builder.add_endpoint("get_item", str, "get")
builder.add_endpoint("create_item", "json", "post")

# Write to disk
with open("my_api.py", "w") as f:
    f.write(builder.get_code())

print("Generated Flask app written to my_api.py")
```

Then run the generated server:

```bash
pip install flask requests
python my_api.py
```

### 6. Mixing JSON and Typed Endpoints

You can mix `"json"` and typed return values in the same builder:

```python
from main import APIBuilder

builder = APIBuilder("mixed_api", "https://api.example.com")

# JSON response — parsed automatically
builder.add_endpoint("get_data", "json", "get")

# String response — raw text
builder.add_endpoint("get_raw", str, "get")

# Integer response — e.g. a status/count endpoint
builder.add_endpoint("get_count", int, "get")

print(builder.get_code())
```

## API Reference

### `APIBuilder(name, url)`

Create a new API builder instance.

| Parameter | Type  | Description                            |
|-----------|-------|----------------------------------------|
| `name`    | `str` | The name of the Flask application      |
| `url`     | `str` | The base URL of the external API       |

### `APIBuilder.add_endpoint(name, returntype, api_type, extra_code="")`

Add a route to the generated Flask app.

| Parameter    | Type                                   | Description                                                                     |
|--------------|----------------------------------------|---------------------------------------------------------------------------------|
| `name`       | `str`                                  | The function/route name                                                         |
| `returntype` | `type \| "json" \| dict[param, type]`  | Return type — `"json"` to parse JSON, or a Python type to cast response text    |
| `api_type`   | `"get" \| "post"`                      | HTTP method                                                                     |
| `extra_code` | `str`                                  | Optional Python code injected before the request                                |

### `APIBuilder.get_code()`

Returns the complete generated Flask application as a Python source string.

## Running the Examples

All examples live in the [`examples/`](examples/) folder:

```bash
# Basic JSON endpoint
python examples/basic_json_api.py

# Multiple endpoints
python examples/multiple_endpoints.py

# Non-JSON string response
python examples/string_response.py

# Extra code injection
python examples/extra_code.py

# Write generated app to a file
python examples/write_to_file.py

# See what generated output looks like
cat examples/simple.py
```

## License

See [pyproject.toml](pyproject.toml) for project metadata.
