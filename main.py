# -*- coding: utf-8 -*-
import os
import pymongo
from bson.json_util import dumps
from bson.regex import Regex
from datetime import datetime, timedelta
from flask import Flask, jsonify, request

from news.news import settings

app = Flask(__name__)


connection = pymongo.MongoClient(
    settings.MONGODB_URI,
)
db = connection[settings.MONGODB_DB]
collection = db[settings.MONGODB_COLLECTION]


@app.route('/bbc')
def bbc_articles():
    title = request.args.get('title', '')
    tag = request.args.get('tag', '')
    try:
        days = int(request.args.get('days_old', 0))
        scraped_date = (datetime.now() - timedelta(days=days)
                        ).strftime("%Y-%m-%d")
        print(scraped_date)
    except TypeError as e:
        scraped_date = datetime.now().strftime("%Y-%m-%d")

    items = collection.find({"$and": [
        {'title': Regex(title)},
        {'tag': Regex(tag)},
        {'scraped_date': scraped_date}
    ]})
    return dumps(items)


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
