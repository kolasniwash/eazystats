from fastapi import APIRouter
from backend.model import GameInput
from backend.queries.insert import (
    insert_into_game_details_query,
    insert_into_player_lineup_query,
    insert_shot_data_ddl
)
from pandas import read_csv
from backend.db import get_postgres_connection

router = APIRouter(
    prefix="/games",
    tags=["games"],
)

def load_local_shots_data(path):
    df = read_csv(path)
    df.to_csv(f"../data/processed/{path.split('/')[-1]}", index=False)
    return df


@router.post("/new")
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