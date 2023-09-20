import json
import config
import orm
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

import repository
from model import Game, PlayingLineup

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


def get_typeform_answer_responses(response):
    return response["form_response"]["answers"]

@app.route("/", methods=["GET"])
def hello():
    return jsonify({'message': 'Hello world!'}), 200

@app.route("/game", methods=["POST"])
def log_game_endpoint():

    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    answers = request.json["form_response"]["answers"]
    form_responses = dict()

    for answer in answers:
        if answer["type"] == "date":
            form_responses[answer["field"]["ref"]] = answer["date"]
        elif answer["type"] == "text":
            form_responses[answer["field"]["ref"]] = answer["text"]
        else:
            form_responses[answer["field"]["ref"]] = answer["choice"]["label"]

    lineup = PlayingLineup(
        lead=form_responses["lead"],
        second=form_responses["second"],
        third=form_responses["third"],
        fourth=form_responses["fourth"],
        skip=form_responses["skip"],
        vice=form_responses["vice"],
        alternate=form_responses["alternate"]
    )

    game = Game(
        event_name=form_responses["event_name"],
        season=form_responses["season"],
        date=form_responses["date"],
        opponent=form_responses["opponent"],
        reg_ends=form_responses["reg_ends"],
        tournament_round=form_responses["tournament_stage"]
    )

    session.add(game)
    session.add(lineup)
    session.commit()

    game_id = session.execute(text("Select max(id), game_id from game_details"))
    lineup_id = session.execute(text("Select max(id), lead from player_lineup"))

    return {"game": game.to_json(),
            "lineup": lineup.to_json(),
            "game_id": game_id,
            "lineup_id": lineup_id,
            "stats-link": form_responses['stats-link']}, 201
