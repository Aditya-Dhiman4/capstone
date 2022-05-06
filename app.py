from flask import Flask, render_template, jsonify

app = Flask(__name__,  template_folder="frontend")

@app.route('/')
def interface():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
