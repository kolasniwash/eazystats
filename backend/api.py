
import pandas as pd
import sqlite3
from fastapi import FastAPI
from backend.routes import games, views
from dotenv import load_dotenv


from backend.query.ops import (
    reset_all_entry_tables,
    create_games_tables,
    create_player_lineup_tables,
    create_shots_tables
)
from backend.query.aggregates import (
    get_shot_counts_query,
    get_player_averages_query
)
from backend.db import get_postgres_connection

app = FastAPI()
load_dotenv()

app.include_router(games.router)
app.include_router(views.router)

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


