from flask import Flask
import requests
from json import loads

app: Flask = Flask(__name__)

def json(x):
    return loads(x)

def test():

    return json(requests.get("https://google.com").text)
