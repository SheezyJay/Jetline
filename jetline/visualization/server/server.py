from flask import Flask
from flask_webgui import FlaskUI  # Import FlaskUI

app = Flask(__name__, static_folder='dist', static_url_path='')

@app.route('/')
def index():
    return "asd"


if __name__ == '__main__':
   app.run()
