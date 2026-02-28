"""
String (Non-JSON) Response Example
===================================

Not every API returns JSON.  When the upstream response is plain text,
HTML, or another non-JSON format you can pass a Python type like ``str``
as the ``returntype`` so the generated code casts the response body
instead of parsing JSON.

Usage:
    python string_response.py
"""

from main import APIBuilder

# httpbin.org/html returns a simple HTML page
builder = APIBuilder("html_fetcher", "https://httpbin.org/html")

# Return the raw HTML as a Python str
builder.add_endpoint("fetch_html", str, "get")

code = builder.get_code()
print(code)
