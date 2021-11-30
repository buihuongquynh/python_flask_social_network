from os import path
from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy


DB_NAME = "database.db"
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'okay'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User, Post, Comment, Follow

    create_database(app)

    return app

def create_database(app):
    if not path.exists('PYTHON_FLASK_SOCIAL_NETWORK/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')