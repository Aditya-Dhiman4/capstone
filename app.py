from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def interface():
    return 'hello'

app.run()
