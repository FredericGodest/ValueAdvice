from flask import Flask
import webscrap

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

print("ok")
