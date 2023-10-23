import os

import pandas as pd
import sqlite3
import psycopg2
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datapane as dp
from matplotlib import pyplot as plt

from app.model import TypeFormResponse
from dotenv import load_dotenv


from contextlib import contextmanager
from app.queries import (
    insert_into_game_details_query,
    insert_into_player_lineup_query,
    reset_all_entry_tables,
    create_games_tables,
    create_player_lineup_tables,
    create_shots_tables,
    insert_shot_data_ddl,
    game_summary_query,
    get_player_position_histogram,
    get_shot_counts_query, get_player_averages_query
)


app = FastAPI()
load_dotenv()


@contextmanager
def get_database_connection(db_name="./data/db/testing.db"):
    connection = sqlite3.connect(db_name)
    try:
        yield connection
    finally:
        connection.close()

def get_postgres_connection_details():
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv("HOST_PORT")
    password = os.environ.get("POSTGRES_PASSWORD", "abc123")
    schema = os.getenv("POSTGRES_SCHEMA")
    user = os.getenv("POSTGRES_USER")
    database = os.getenv("POSTGRES_DB")
    return database, user, password, host, port, schema

@contextmanager
def get_postgres_connection():
    database, user, password, host, port, schema = get_postgres_connection_details()

    connection = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    try:
        yield connection
    finally:
        connection.close()

def setup_tables(reset_tables=False):
    with get_postgres_connection() as conn:
    # with get_database_connection() as conn:
        cursor = conn.cursor()
        if reset_tables:
            reset_all_entry_tables(cursor)
            conn.commit()

        create_games_tables(cursor)
        create_player_lineup_tables(cursor)
        create_shots_tables(cursor)
        conn.commit()


setup_tables(reset_tables=False)



def run_query(query, db):
    with sqlite3.connect(db) as conn:
        return pd.read_sql(query, conn)

@app.get("/")
async def root():
    return {"message": "Hello World"}

def save_shot_data_csv(sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=ShotDataInput"
    df = pd.read_csv(url)
    df.to_csv(f"./data/drop/shot-data-input-{sheet_id}.csv", index=False)
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


    #with get_database_connection() as conn:
    with get_postgres_connection() as conn:
        cursor = conn.cursor()

        game_details_query = insert_into_game_details_query(**form_responses)
        print(game_details_query)
        cursor.execute(game_details_query)
        game_id = cursor.fetchone()[0]
        conn.commit()

        positions = ['lead', 'second', 'third', 'fourth', 'alternate']
        players = ['luis', 'nico', 'mikel', 'sergio', 'edu']
        for position, player in zip(positions, players):
            player_lineup_query = insert_into_player_lineup_query(game_id, position, player)
            print(player_lineup_query)
            cursor.execute(player_lineup_query)
            conn.commit()

    df_shots = save_shot_data_csv(form_responses["sheet_id"])

    # with get_database_connection() as conn:
    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        df_shots["game_id"] = game_id
        df_shots.dropna(inplace=True)
        for item in df_shots.iterrows():
            insert_shot_data_query = insert_shot_data_ddl(item[1])
            cursor.execute(insert_shot_data_query)
        conn.commit()

    return {"game_details": form_responses, "game_id": game_id}


@app.get("/eazystats/v1/shot_counts")
async def shot_counts_view():

    with get_postgres_connection() as conn:
        shot_counts = pd.read_sql(get_shot_counts_query(), conn)

    shot_counts = shot_counts.set_index("player").astype(int)
    shot_count_norm = shot_counts.div(shot_counts.sum(axis=1), axis=0) * 100

    ax = shot_count_norm.plot.bar(stacked=True, figsize=(3, 2), legend=False, fontsize=7)
    ax_counts = shot_counts.plot.bar(stacked=True, figsize=(3, 2), legend=False, secondary_y=True, ax=ax, fontsize=7)
    ax.legend(title="Scores", fontsize=7, loc='upper left', bbox_to_anchor=(1.2, 1))
    ax.set_title("How to make more 3s and 4s?", fontsize=7)
    ax.set_xlabel("Player name", fontsize=7)
    ax.set_ylabel("% Shots", fontsize=7)
    ax_counts.set_ylabel("No. Shots", fontsize=7)

    for bar in ax_counts.patches:
        bar.set_facecolor('none')


    view = dp.Group(
        blocks=[
            dp.HTML("<h1>How many of each shot score are we making?</h1>"),
            dp.Plot(ax),
            dp.HTML("<h3>Score count by player</h3>"),
            dp.DataTable(shot_counts, label="Game shot counts")
            ]
    )

    dp.save_report(view, "./shot-counts-tallinn.html")
    html = dp.stringify_report(view)
    return HTMLResponse(content=html, status_code=200)


@app.get("/eazystats/v1/summary/games")
async def get_stats_summary():
    """Table with each game and a player % total in each game
    + team total + team total zeros + made after miss"""

    with get_database_connection() as conn:
        games_summary = pd.read_sql(game_summary_query(), conn)

    view = dp.Group(
        blocks=[
            dp.HTML("<h1> Team Vez Playing Statistics </h1>"),
            dp.HTML("<h3> Game Summaries by Position </h3>"),
            dp.DataTable(games_summary, label="Game Summaries by Position"),
            ]
    )

    html = dp.stringify_report(view)
    return HTMLResponse(content=html, status_code=200)

@app.get("/eazystats/v1/performance")
async def player_position_histogram():


    with get_postgres_connection() as conn:
        player_avg = pd.read_sql(get_player_averages_query(), conn)

    view_averages = player_avg.pivot(columns='player', values='average')
    ax_averages = view_averages.plot(kind='box', figsize=(6, 3), fontsize=7)

    # Customize the chart (optional)
    ax_averages.set_title('Range of game scoring averages', fontsize=7)
    ax_averages.set_xlabel('Player', fontsize=7)
    ax_averages.set_ylabel('Score', fontsize=7)
    ax_averages.set_yticks(range(0, 5))

    fig, axes = plt.subplots(1, 2, figsize=(6, 3))

    view_out = player_avg.pivot(columns='player', values='out_average')
    ax_out = view_out.plot(kind='box', ax=axes[0], widths=0.5, fontsize=7)

    # Customize the chart (optional)
    ax_out.set_title('Averages - OUT TURN', fontsize=7)
    ax_out.set_xlabel('Player', fontsize=7)
    ax_out.set_ylabel('Score', fontsize=7)
    ax_out.set_yticks(range(0, 5))


    view_in = player_avg.pivot(columns='player', values='in_average')
    ax_in = view_in.plot(kind='box', ax=axes[1], widths=0.5, fontsize=7)
    ax_in.set_title('Averages - IN TURN', fontsize=7)
    ax_in.set_xlabel('Player', fontsize=7)
    ax_in.set_ylabel('Score', fontsize=7)
    ax_in.set_yticks(range(0, 5))


    view = dp.Group(
        blocks=[
            dp.HTML("<h1>How big a range is there between our games?</h1>"),
            dp.Plot(ax_averages),
            dp.Plot(fig),
            dp.HTML("<h3>Game averages by player</h3>"),
            dp.DataTable(player_avg, label="Game shot counts")
            ]
    )

    dp.save_report(view, "./performance-tallinn.html")
    html = dp.stringify_report(view)
    return HTMLResponse(content=html, status_code=200)

