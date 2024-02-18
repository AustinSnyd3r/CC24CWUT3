from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', static_url_path='/static')

if __name__ == '__main__':
    app.run(debug=True)