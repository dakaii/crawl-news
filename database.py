import pymongo

from news.news import settings


def setup_db():
    connection = pymongo.MongoClient(
        settings.MONGODB_URI,
    )
    db = connection[settings.MONGODB_DB]
    return db[settings.MONGODB_COLLECTION]
