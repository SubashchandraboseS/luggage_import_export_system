# app.py
from flask import Flask
from config import Config
from models import db
from views import init_app

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
