# -*- coding: utf-8 -*-
from bson.json_util import dumps
from bson.regex import Regex
from flask import Flask, request

from database import setup_db
from helper import get_scraped_date

app = Flask(__name__)

collection = setup_db()

@app.route('/bbc')
def bbc_articles():
    title = request.args.get('title', '')
    tag = request.args.get('tag', '')
    scraped_date = get_scraped_date(request)

    items = collection.find({"$and": [
        {'title': Regex(title)},
        {'tag': Regex(tag)},
        {'scraped_date': scraped_date}
    ]})
    return dumps(items.count())


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
