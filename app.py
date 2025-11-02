import os
from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

sample = Flask(__name__)

mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
db = client[db_name]
routers = db["routers"]

@sample.route("/")
def main():
    all_devices = list(routers.find())
    return render_template("index.html", data=all_devices)

@sample.route("/add_device", methods=["POST"])
def add_device():
    router_ip = request.form.get("router_ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if router_ip and username and password:
        routers.insert_one({
            "router_ip": router_ip,
            "username": username,
            "password": password
        })
    return redirect(url_for("main"))

@sample.route("/delete_device", methods=["POST"])
def delete_device():
    try:
        device_id_str = request.form.get("device_id")
        routers.delete_one({"_id": ObjectId(device_id_str)})
    except Exception as e:
        print(f"Error deleting device: {e}")
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)