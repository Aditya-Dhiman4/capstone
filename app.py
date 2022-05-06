from flask import Flask, request

app = Flask(__name__)

@app.data('/')
def interface():
    print('hello')

app.run()
