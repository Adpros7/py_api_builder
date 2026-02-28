"""
Write Generated Code to a File
================================

A complete end-to-end example that:
  1. Builds an API with multiple endpoints
  2. Writes the generated Flask app to a ``.py`` file
  3. Shows how you could run the generated app

Usage:
    python write_to_file.py          # generates my_api.py
    python my_api.py                 # (would) start the Flask server

Note:
    The generated file requires ``flask`` and ``requests`` to be installed.
"""

import os
from main import APIBuilder

# --- Build the API ---
builder = APIBuilder("my_api", "https://api.example.com/v1/data")

builder.add_endpoint("list_items", "json", "get")
builder.add_endpoint("get_item", str, "get")
builder.add_endpoint("create_item", "json", "post")

# --- Write to disk ---
output_path = os.path.join(os.path.dirname(__file__), "my_api.py")
code = builder.get_code()

with open(output_path, "w") as f:
    f.write(code)

print(f"Generated Flask app written to: {output_path}")
print()
print("To run the generated server:")
print("  1. pip install flask requests")
print(f"  2. python {output_path}")
