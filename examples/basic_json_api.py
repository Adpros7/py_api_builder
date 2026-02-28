"""
Basic JSON API Example
======================

The simplest use case: generate a Flask app that fetches JSON data
from an external API and returns it as-is.

This example builds a single GET endpoint that proxies requests to the
JSONPlaceholder API (a free fake REST API for testing).

Generated output (written to ``basic_json_api_output.py``)::

    from flask import Flask
    import requests
    from json import loads
    from typing import TypeAlias

    app: Flask = Flask(__name__)

    def get_posts() -> ...:
        return (requests.get('https://jsonplaceholder.typicode.com/posts').json)

Usage:
    python basic_json_api.py
"""

from main import APIBuilder

# 1. Create a builder pointing at the JSONPlaceholder API
builder = APIBuilder("jsonplaceholder", "https://jsonplaceholder.typicode.com/posts")

# 2. Add a single GET endpoint that returns JSON
builder.add_endpoint("get_posts", "json", "get")

# 3. Retrieve and display the generated code
code = builder.get_code()
print(code)

# 4. Optionally, write it to a file
with open("basic_json_api_output.py", "w") as f:
    f.write(code)
    print("\nGenerated code written to basic_json_api_output.py")
