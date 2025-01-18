from flask import Blueprint, request, jsonify
import app.models.arena as arena
from app.models.movie_list import Movie_list


main = Blueprint("main", __name__)


@main.route("/get_arena_json", methods = ["GET"])
def get_arena_json():
    new_arena = arena.build_arena()
    return new_arena.to_json()


@main.route("/get_all_ratings", methods = ["GET"])
def get_all_ratings():
    movie_list = Movie_list()
    return movie_list.to_json()


@main.route("/post_winner", methods = ["POST"])
def post_winner():
    arena_res = request.get_json()
    if not arena_res:
        return jsonify({"Error: No data provided"}), 400
    
    winner = arena_res.get("winner")
    if winner is None:
        return jsonify({"error": "Winner not provided"}), 400
    print(f"Winner received: {winner}")
    
    new_arena = arena.set_arena_from_post(arena_res)
    arena.save_new_scores(new_arena)

    return jsonify({"message": "Winner received successfully", "winner": winner})