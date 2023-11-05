import os
import pandas as pd
import sqlite3
import psycopg2
from fastapi import FastAPI, Request

from model import GameInput
from dotenv import load_dotenv

from contextlib import contextmanager
from queries.insert import (
    insert_into_game_details_query,
    insert_into_player_lineup_query,
    insert_shot_data_ddl
)
from queries.ops import (
    reset_all_entry_tables,
    create_games_tables,
    create_player_lineup_tables,
    create_shots_tables
)

from queries.aggregates import (
    get_shot_counts_query,
    get_player_averages_query
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

def load_local_shots_data(path):
    df = pd.read_csv(path)
    df.to_csv(f"../data/processed/{path.split('/')[-1]}", index=False)
    return df


@app.post("/eazystats/v1/games/new")
async def input_new_game(game: GameInput):
    game_dict = dict(game)

    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        game_details_query = insert_into_game_details_query(**game_dict)
        cursor.execute(game_details_query)
        game_id = cursor.fetchone()[0]
        conn.commit()

        positions = ["lead", "second", "third", "fourth", "alternate"]
        for position in positions:
            player_lineup_query = insert_into_player_lineup_query(game_id, position, game_dict[position])
            print(player_lineup_query)
            cursor.execute(player_lineup_query)
            conn.commit()

    df_shots = load_local_shots_data(game_dict["file"])

    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        df_shots["game_id"] = game_id
        df_shots.dropna(inplace=True, subset="SCORE")
        for item in df_shots.iterrows():
            insert_shot_data_query = insert_shot_data_ddl(item[1])
            cursor.execute(insert_shot_data_query)
        conn.commit()

    return {"game_details": game_dict, "game_id": game_id}


@app.get("/eazystats/v1/shot_counts/data")
async def shot_counts_data(request: Request):

    kwargs = request.query_params
    query = get_shot_counts_query(**kwargs)
    print(query)
    with get_postgres_connection() as conn:
        shot_counts = pd.read_sql(query, conn)

    shot_counts = shot_counts.set_index("player").astype(int)
    shot_count_norm = shot_counts.div(shot_counts.sum(axis=1), axis=0) * 100

    return {"data": shot_count_norm.to_json()}



@app.get("/eazystats/v1/summary/data")
async def summary_data(request: Request):

    kwargs = request.query_params
    query = get_player_averages_query(**kwargs)

    with get_postgres_connection() as conn:
        player_avg = pd.read_sql(query, conn)

    return {"data": player_avg.to_json()}
