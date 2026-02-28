"""
Multiple Endpoints Example
===========================

Demonstrates building a Flask app with several endpoints that each
proxy a different path on the same external API.

This is useful when you want to expose a curated subset of an
upstream REST API through your own Flask server.

Usage:
    python multiple_endpoints.py
"""

from main import APIBuilder

# Point at the JSONPlaceholder fake REST API
builder = APIBuilder("blog_api", "https://jsonplaceholder.typicode.com")

# --- Add multiple GET endpoints ---

# Fetch all posts as JSON
builder.add_endpoint("get_posts", "json", "get")

# Fetch all comments as JSON
builder.add_endpoint("get_comments", "json", "get")

# Fetch all users as JSON
builder.add_endpoint("get_users", "json", "get")

# --- Add a POST endpoint ---

# Create a new post (upstream returns the created resource as JSON)
builder.add_endpoint("create_post", "json", "post")

# --- Output ---
code = builder.get_code()
print(code)
print("\n# ---- Summary ----")
print("# Endpoints generated: get_posts, get_comments, get_users, create_post")
