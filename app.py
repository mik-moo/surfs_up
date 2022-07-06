from asyncio.base_futures import _format_callbacks
from cProfile import run


# Import flask
from flask import Flask
from psutil import users

# create flask instance
app = Flask(__name__)

#create flask route and write a function
# @app.route('/')
# def hello_world():
#     return 'Hello world' 


# Create skill drill route

@app.route('/')
def profile():
    n = input("Username?")
    return 'Hello' + n

