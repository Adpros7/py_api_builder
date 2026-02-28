"""
Extra Code Injection Example
==============================

The ``extra_code`` parameter lets you inject arbitrary Python statements
into the generated endpoint function *before* the API request is made.

Common use cases:
  - Logging / print statements for debugging
  - Setting up headers or authentication tokens
  - Validating preconditions

Usage:
    python extra_code.py
"""

from main import APIBuilder

builder = APIBuilder("debug_api", "https://jsonplaceholder.typicode.com/posts")

# Inject a print statement that runs every time the endpoint is called
builder.add_endpoint(
    name="get_posts_debug",
    returntype="json",
    api_type="get",
    extra_code='print("Fetching posts...")',
)

# Inject a logging call instead
builder.add_endpoint(
    name="get_posts_logged",
    returntype="json",
    api_type="get",
    extra_code='import logging; logging.info("GET /posts called")',
)

code = builder.get_code()
print(code)
