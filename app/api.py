import pandas as pd
import sqlite3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datapane as dp
from app.model import TypeFormResponse

from contextlib import contextmanager
from app.queries import (
    insert_into_game_details_query,
    insert_into_player_lineup_query,
    reset_all_entry_tables,
    create_games_tables,
    create_player_lineup_tables,
    create_shots_tables,
    insert_shot_data_ddl
)


app = FastAPI()



@contextmanager
def get_database_connection(db_name="./data/db/testing.db"):
    connection = sqlite3.connect(db_name)
    try:
        yield connection
    finally:
        connection.close()


def setup_tables(reset_tables=False):
    with get_database_connection() as conn:
        cursor = conn.cursor()
        if reset_tables:
            reset_all_entry_tables(cursor)
            conn.commit()

        create_games_tables(cursor)
        create_player_lineup_tables(cursor)
        create_shots_tables(cursor)
        conn.commit()


setup_tables(reset_tables=False)

@app.get("/")
async def root():
    return {"message": "Hello World"}

def save_shot_data_csv(sheet_id, sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    df.to_csv(f"./data/drop/{sheet_name}.csv", index=False)
    return df

@app.post("/eazystats/v1/games/add")
async def add_game_detail(item: TypeFormResponse):
    answers = item.form_response.answers
    form_responses = dict()

    for answer in answers:
        if answer.type == "date":
            form_responses[answer.field.ref] = answer.date
        elif answer.type == "text":
            form_responses[answer.field.ref] = answer.text
        else:
            form_responses[answer.field.ref] = answer.choice.label


    with get_database_connection() as conn:
        cursor = conn.cursor()

        game_details_query = insert_into_game_details_query(**form_responses)
        print(game_details_query)
        cursor.execute(game_details_query)
        game_id = cursor.lastrowid
        conn.commit()

        player_lineup_query = insert_into_player_lineup_query(game_id, **form_responses)
        cursor.execute(player_lineup_query)
        conn.commit()

    df_shots = save_shot_data_csv(form_responses["sheet_id"], form_responses["sheet_name"])

    with get_database_connection() as conn:
        cursor = conn.cursor()
        for item in df_shots.values.tolist():
            item.insert(0, game_id)
            cursor.execute(insert_shot_data_ddl(), item)
        conn.commit()

    return {"game_details": form_responses, "game_id": game_id}


@app.get("/eazystats/v1/stats/")
async def get_stats():

    view = dp.Group(
        blocks=[
        dp.HTML("<h1> Team Vez Playing Statistics </h1>"),
        dp.HTML("<h3> Game Summaries by Position </h3>"),
        dp.HTML("<h3> Shot Making by Turn, Player, and Position </h3>")]
    )

    html = dp.stringify_report(view)

    return HTMLResponse(content=html, status_code=200)

@app.get("/eazystats/v1/stats/aggregates/by-position")
async def get_aggregate_position_stats():
    def run_query(query, db):
        with sqlite3.connect(db) as conn:
            return pd.read_sql(query, conn)

    # position_stats_query = get_aggregate_position_stats_query()
    with get_database_connection() as conn:

        query = """SELECT game_id, thrower_position, avg(score) from shots_table group by game_id, thrower_position;"""
        position_stats = pd.read_sql(query, conn)

    view = dp.Group(
        blocks=[
        dp.HTML("<h1> Team Vez Playing Statistics </h1>"),
        dp.HTML("<h3> Game Summaries by Position </h3>"),
        dp.DataTable(position_stats, label="Game Summaries by Position"),
        dp.HTML("<h3> Shot Making by Turn, Player, and Position </h3>")]
    )

    html = dp.stringify_report(view)

    return HTMLResponse(content=html, status_code=200)



#
# @app.get("/v1/stats/aggregates/player-breakdown")
# async def get_aggregate_player_breakdown():
#     db = './data/db/games_data_test.db'
#
#     query = player_breakdown_stats_query
#     with sqlite3.connect(db) as conn:
#         cur = conn.cursor()
#         result = cur.execute(query)
#         all_results = result.fetchall()
#
#     print(all_results)
#
#     return {"player-breakdown": all_results}
#
# @app.get("/v1/stats/aggregates/position-breakdown")
# async def get_aggregate_position_breakdown():
#     db = './data/db/games_data_test.db'
#
#     query = position_breakdown_stats_query
#     with sqlite3.connect(db) as conn:
#         cur = conn.cursor()
#         result = cur.execute(query)
#         all_results = result.fetchall()
#
#     print(all_results)
#
#     return {"position-breakdown": all_results}
#
#
# @app.get("/v1/stats/aggregates/position-stats")
# async def get_aggregate_position_stats():
#     db = './data/db/games_data_test.db'
#
#     query = position_stats_query
#     with sqlite3.connect(db) as conn:
#         cur = conn.cursor()
#         result = cur.execute(query)
#         all_results = result.fetchall()
#
#     print(all_results)
#
#     return {"position-stats": all_results}
#
# position_stats_query = """
#         WITH game_aggregates AS (
#         SELECT
#             game_id,
#             ROUND(AVG(score) filter (where thrower_position = 'lead') * 100 / 4, 2)  AS lead,
#             ROUND(AVG(score) filter (where thrower_position = 'second') * 100 / 4, 2)  AS second,
#             ROUND(AVG(score) filter (where thrower_position = 'third') * 100 / 4, 2)  AS third,
#             ROUND(AVG(score) filter (where thrower_position = 'fourth') * 100 / 4, 2)  AS fourth,
#             ROUND(AVG(score)*100 / 4, 1) AS team_pct
#         FROM shots_table
#         GROUP BY game_id
#         )
#         SELECT
#             gd.event_name,
#             gd.opponent,
#             ga.lead,
#             ga.second,
#             ga.third,
#             ga.fourth,
#             ga.team_pct
#         FROM game_aggregates AS ga
#         LEFT JOIN game_details AS gd ON ga.game_id = gd.game_id;"""
#
#
# position_breakdown_stats_query = """
#         SELECT
#             thrower_position as Position,
#             ROUND(AVG(score) filter (where draw_or_hit = 'D' and turn = 'IN') * 100 / 4, 2)  AS 'In Turn Draws',
#             ROUND(AVG(score) filter (where draw_or_hit = 'H' and turn = 'IN') * 100 / 4, 2)  AS 'In Turn Hits',
#             ROUND(AVG(score) filter (where draw_or_hit = 'D' and turn = 'OUT') * 100 / 4, 2)  AS 'Out Turn Draws',
#             ROUND(AVG(score) filter (where draw_or_hit = 'H' and turn = 'OUT') * 100 / 4, 2)  AS 'Out Turn Hits',
#             ROUND(AVG(score) filter (where draw_or_hit = 'D') * 100 / 4, 2)  AS 'Total Draws',
#             ROUND(AVG(score) filter (where draw_or_hit = 'H') * 100 / 4, 2)  AS 'Total Hits'
#         FROM shots_table
#         GROUP BY thrower_position;
# """
#
# player_breakdown_stats_query = """
#         SELECT
#             thrower_name as Player,
#             ROUND(AVG(score) filter (where draw_or_hit = 'D' and turn = 'IN') * 100 / 4, 2)  AS 'In Turn Draws',
#             ROUND(AVG(score) filter (where draw_or_hit = 'H' and turn = 'IN') * 100 / 4, 2)  AS 'In Turn Hits',
#             ROUND(AVG(score) filter (where draw_or_hit = 'D' and turn = 'OUT') * 100 / 4, 2)  AS 'Out Turn Draws',
#             ROUND(AVG(score) filter (where draw_or_hit = 'H' and turn = 'OUT') * 100 / 4, 2)  AS 'Out Turn Hits',
#             ROUND(AVG(score) filter (where draw_or_hit = 'D') * 100 / 4, 2)  AS 'Total Draws',
#             ROUND(AVG(score) filter (where draw_or_hit = 'H') * 100 / 4, 2)  AS 'Total Hits'
#         FROM shots_table
#         GROUP BY thrower_name;
# """