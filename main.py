from typing import Any, Literal, TypeAlias

param: TypeAlias = str
returnType: TypeAlias = type | Literal["json"]


class APIBuilder:
    def __init__(self, name: str, url: str) -> None:
        """
        Initializes the API builder.

        Parameters:
            name (str): The name of the API.
            url (str): The URL of the API.

        Returns:
            None
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
    ):
        """
        Adds an endpoint to the API.

        Parameters:
            name (str): The name of the endpoint.
            returntype (type | Literal["json"]): The type of the data returned by the endpoint. Alternatively, a dictionary mapping parameter names to return types. This is used for over loading.
            api_type (Literal["get", "post"]): The type of the API request.
            extra_code (str): Any extra code to run before making the request.

        Returns:
            None
        """
        self.code += f"""
        def {name}() -> {returntype}:
            {extra_code}
            return {returntype if returntype != "json" else ""}(requests.{api_type}({self.url}).{"text" if returntype != "json" else "json"})
        """

    def create_returntype(self, name: str, x: Any):
        pass
    def get_code(self):
        """
        Returns the code for the API.
        """

        return self.code


if __name__ == "__main__":
    build: APIBuilder = APIBuilder("test", "https://google.com")
    build.add_endpoint("test", "json", "get")
    print(build.get_code())
