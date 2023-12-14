import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from mongo_client import mongo_client
from jsonify_mongo_cursor import jsonify_mongo_cursor

load_dotenv(dotenv_path="./.env.local")

UNSPLASH_URL = "https://api.unsplash.com/photos/random"
UNSPLASH_KEY = os.environ.get("UNSPLASH_KEY", "")
DEBUG = os.environ.get("DEBUG", "True") == "True"

if not UNSPLASH_KEY:
    raise EnvironmentError(
        "Please create .env.local file and insert UNSPLASH_KEY as environment variable"
    )

gallery = mongo_client.gallery
images_collection = gallery.images

app = Flask(__name__)
CORS(app)


@app.route("/new-image")
def new_image():
    word = request.args.get("query")
    headers = {"Accept-Version": "v1", "Authorization": "Client-ID " + UNSPLASH_KEY}
    params = {"query": word}

    response = requests.get(
        url=UNSPLASH_URL, headers=headers, params=params, timeout=10
    )

    data = response.json()
    return data


@app.route("/images", methods=["GET", "POST"])
def images():
    if request.method == "GET":
        # read images from the database
        allimages = images_collection.find({})
        print(type(allimages))
        return jsonify_mongo_cursor(allimages)

    if request.method == "POST":
        # save image to the database
        image = request.get_json()
        if images_collection.count_documents({"id": image.get("id")}, limit=1):
            return jsonify_mongo_cursor(
                images_collection.update_one({"id": image.get("id")}, {"$set": image})
            )
        else:
            res = images_collection.insert_one(image)
            return jsonify_mongo_cursor(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=DEBUG)
