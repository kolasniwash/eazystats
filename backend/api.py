import os
import pandas as pd
import sqlite3
import psycopg2
from fastapi import FastAPI, Request
from backend.routes.post_game import games
from dotenv import load_dotenv

from contextlib import contextmanager


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
from backend.db import get_postgres_connection

app = FastAPI()
load_dotenv()

app.include_router(games.router)

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
