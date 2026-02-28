"""
py-api-builder: A code generator for creating Flask API wrappers.

This module provides the ``APIBuilder`` class, which programmatically
generates Flask application code that proxies requests to an external API.
It supports GET and POST endpoints with configurable return types.

Type Aliases:
    param: Alias for ``str``, representing an endpoint parameter name.
    returnType: Alias for ``type | Literal["json"]``, representing the
        return type of a generated endpoint. Use a Python type (e.g. ``str``,
        ``int``) to cast the response text, or ``"json"`` to parse the
        response as JSON.
"""

from typing import Any, Literal, TypeAlias

param: TypeAlias = str
"""Alias for ``str`` — an endpoint parameter name."""

returnType: TypeAlias = type | Literal["json"]
"""Alias for ``type | Literal["json"]`` — the return type of a generated endpoint."""


class APIBuilder:
    """A code generator that builds Flask applications proxying an external API.

    ``APIBuilder`` accumulates Python source code for a Flask app.  Call
    :meth:`add_endpoint` one or more times to register routes, then call
    :meth:`get_code` to retrieve the complete generated source.

    Attributes:
        code (str): The accumulated Python source code for the Flask app.
        url (str): The quoted URL of the external API, ready for embedding
            in the generated source.

    Example::

        builder = APIBuilder("my_api", "https://api.example.com/data")
        builder.add_endpoint("fetch_data", "json", "get")
        print(builder.get_code())
    """

    def __init__(self, name: str, url: str) -> None:
        """Initialize the API builder.

        Args:
            name: The name of the Flask application.
            url: The base URL of the external API to proxy.
        """
        self.code: str = f"""
        from flask import Flask
        import requests
        from json import loads
        from typing import TypeAlias

        app: Flask = Flask(__name__)
        """
        self.url: str = "'" + url + "'"

    def add_endpoint(
        self,
        name: str,
        returntype: returnType | dict[param, returnType],
        api_type: Literal["get", "post"],
        extra_code: str = "",
    ) -> None:
        """Add a Flask route that proxies a request to the external API.

        The generated function will issue an HTTP request using the
        ``requests`` library and cast or parse the response according to
        *returntype*.

        Args:
            name: The function (and route) name for the generated endpoint.
            returntype: The return type of the endpoint.  Pass a Python type
                (e.g. ``str``) to cast the response text, or ``"json"`` to
                parse the response as JSON.  A ``dict[param, returnType]``
                can be provided for overloaded endpoints.
            api_type: The HTTP method to use — ``"get"`` or ``"post"``.
            extra_code: Optional Python source to insert before the request
                call inside the generated function body.
        """
        if not isinstance(returntype, dict):
            self.code += f"""
            def {name}() -> {returntype}:
                {extra_code}
                return {returntype if returntype != "json" else ""}(requests.{api_type}({self.url}).{"text" if returntype != "json" else "json"})


            """

        else:
            self.code += f"""
            """

    def create_returntype(self, name: str, x: Any) -> None:
        """Create a custom return type for use in generated endpoints.

        .. note::
            This method is not yet implemented.

        Args:
            name: The name of the custom
            type to define.
            x: The value or schema used to derive the type.
        """
        pass

    def get_code(self) -> str:
        """Return the complete generated Flask application source code.

        Returns:
            The accumulated Python source as a single string, ready to be
            written to a ``.py`` file or executed.

        Example::

            builder = APIBuilder("weather", "https://api.weather.com/v1")
            builder.add_endpoint("current", "json", "get")
            builder.add_endpoint("forecast", str, "get")

            # Write to a file
            with open("weather_api.py", "w") as f:
                f.write(builder.get_code())

            # Or just print it
            print(builder.get_code())
        """
        return self.code


if __name__ == "__main__":
    build: APIBuilder = APIBuilder("test", "https://google.com")
    build.add_endpoint("test", "json", "get")
    print(build.get_code())
