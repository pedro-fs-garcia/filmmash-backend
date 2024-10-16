from flask import Flask
import database

app = Flask(__name__)


@app.route("/get_arena_json", methods = ["GET"])
def get_arena_json():
    new_arena = database.build_arena()
    return new_arena.to_json()


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = "5000", debug = True)