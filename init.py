import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request,_request_ctx_stack
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import spacy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bcrypt = Bcrypt(app)
db_path = 'news.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



