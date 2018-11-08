# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.articles


@app.route('/bbc')
def bbc_articles():

    _items = db.articles.find()
    items = [item for item in _items]

    return jsonify()


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
