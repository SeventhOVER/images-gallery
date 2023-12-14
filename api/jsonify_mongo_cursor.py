from flask import jsonify
from pymongo.cursor import Cursor
from bson.objectid import ObjectId


def jsonify_mongo_cursor(mongo_cursor):
    """jsonify mongo cursor. handle objectid"""
    if isinstance(mongo_cursor, Cursor):
        items = []
        for item in mongo_cursor:
            if isinstance(item.get("_id"), ObjectId):
                item["_id"] = str(item.get("_id"))
            items.append(item)
        return jsonify(items)

    else:
        my_dict = {}
        for prop in dir(mongo_cursor):
            if not prop.startswith("_"):
                if isinstance(mongo_cursor.__getattribute__(prop), ObjectId):
                    my_dict[prop] = str(mongo_cursor.__getattribute__(prop))
                else:
                    my_dict[prop] = mongo_cursor.__getattribute__(prop)

        return jsonify(my_dict)
