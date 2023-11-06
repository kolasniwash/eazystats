import glob
import os
import shutil
import sqlite3
from pathlib import Path

import pandas as pd

def read_game_data(game_data_path):
    # Define the lists to store the game details and playing lineup
    game_details = []
    playing_lineup = []
    # Define the flag to check the current section
    in_game_details = False
    in_playing_lineup = False

    # Open the CSV file and iterate over lines
    with open(game_data_path) as file:
        for line in file:
            # Remove the trailing newline character and split the line by comma
            row = line.strip().split(',')

            if row[0] == 'Game Details':
                # If the current line is the header of the game details section, start storing the game details
                in_game_details = True
                in_playing_lineup = False
                continue
            elif row[0] == 'Playing Lineup':
                # If the current line is the header of the playing lineup section, start storing the playing lineup
                in_playing_lineup = True
                in_game_details = False
                continue

            if in_game_details:
                # If we are in the game details section, store the current row in the game details list
                game_details.append(row)
            elif in_playing_lineup:
                # If we are in the playing lineup section, store the current row in the playing lineup list
                playing_lineup.append(row)

    return game_details, playing_lineup

def read_shot_data(shots_data_path):
    df_shot_data = pd.read_csv(shots_data_path)
    df_shot_data.dropna(inplace=True, subset="shot_type")
    return df_shot_data


def process_game_data(game_details, playing_lineup):
    # Convert the lists to dataframes
    df_game_details = pd.DataFrame(game_details[1:], columns=game_details[0])
    df_playing_lineup = pd.DataFrame(playing_lineup[1:], columns=playing_lineup[0])

    return df_game_details, df_playing_lineup


def connect_to_games_database():
    conn = sqlite3.connect('../data/db/games_data_test.db')
    cursor = conn.cursor()
    return conn, cursor


def create_games_tables(cursor):
    """ Executes DDL statements and creates tables in the database """
    game_details_ddl = """
    CREATE TABLE IF NOT EXISTS game_details (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name VARCHAR(255),
    season VARCHAR(255),
    date DATE,
    opponent VARCHAR(255),
    type VARCHAR(255),
    total_ends INTEGER,
    stage VARCHAR(255),
    UNIQUE (event_name, season, opponent, stage)
    );
    """

    player_lineup_ddl = """
    CREATE TABLE IF NOT EXISTS player_lineup (    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    lead VARCHAR(255),
    second VARCHAR(255),
    third VARCHAR(255),
    fourth VARCHAR(255),
    vice VARCHAR(255),
    skip VARCHAR(255),
    alternate VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES game_details (game_id)
    );
    """

    # cursor.execute("DROP TABLE IF EXISTS game_details")
    cursor.execute(game_details_ddl)

    # cursor.execute("DROP TABLE IF EXISTS player_lineup")
    cursor.execute(player_lineup_ddl)

def create_shots_tables(cursor):
    create_shots_table_ddl = """
    CREATE TABLE IF NOT EXISTS shots_table (
    shot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    end INTEGER,
    throw_in_end INTEGER,
    thrower_position VARCHAR(255),
    thrower_name VARCHAR(255),
    shot_type VARCHAR(255),
    turn VARCHAR(255),
    difficulty INTEGER,
    score INTEGER,
    execution VARCHAR(255),
    line VARCHAR(255),
    release_direction VARCHAR(255),
    release_rotation VARCHAR(255),
    speed VARCHAR(255),
    sweeping VARCHAR(255),
    cleaning BOOLEAN,
    sweeping_infraction VARCHAR(255),
    thrower_stability VARCHAR(255),
    ice_given VARCHAR(255),
    draw_or_hit VARCHAR(255),
    UNIQUE (shot_id, game_id, end, throw_in_end)
    );"""

    # cursor.execute("DROP TABLE IF EXISTS shots_table")
    cursor.execute(create_shots_table_ddl)

def load_game_details(cursor, df_game_details):
    # Write the dataframes to SQLite tables
    insert_game_details_ddl = """INSERT INTO game_details (
        event_name, season, date, opponent, type, total_ends, stage) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (event_name, season, opponent, stage) DO NOTHING;"""
    cursor.execute(insert_game_details_ddl, tuple(df_game_details.values[0]))
    return cursor.lastrowid

def load_player_lineup(cursor, df_playing_lineup, game_id):
    insert_player_lineup_ddl = """
    INSERT INTO player_lineup (
    game_id, lead, second, third, fourth, vice, skip, alternate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

    player_lineup_values = df_playing_lineup.values.tolist()[0]
    player_lineup_values.insert(0, game_id)
    cursor.execute(insert_player_lineup_ddl, tuple(player_lineup_values))


def load_shot_data(cursor, df_shot_data, game_id):
    insert_shot_data_ddl = """
    INSERT INTO shots_table (
    game_id, end, throw_in_end, thrower_position, thrower_name,
    shot_type, turn, difficulty, score, execution, line, 
    release_direction, release_rotation, speed, 
    sweeping, cleaning, sweeping_infraction, 
    thrower_stability, ice_given, draw_or_hit)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""


    for item in df_shot_data.values.tolist():
        item.insert(0, game_id)
        cursor.execute(insert_shot_data_ddl, item)

def find_matching_files(path, pattern):
    pattern = f"{path}/**/*{pattern}*"
    matching_files = glob.glob(pattern, recursive=True)
    return matching_files

def move_file_to_processed_folder(source_path, destination_path="./data/processed"):
    file_name = os.path.basename(source_path)
    print("base path ", file_name)
    new_destination_path = os.path.join(destination_path, file_name)
    shutil.move(source_path, new_destination_path)


def run(data_path):

    for game_data_path in find_matching_files(data_path, "GameData"):
        print(game_data_path)
        search_glob = Path(game_data_path).name.replace("GameData", "ShotData")
        shot_data_path = find_matching_files(data_path, search_glob)[0]
        print(shot_data_path)

        game_details, playing_lineup = read_game_data(game_data_path)
        df_game_details, df_playing_lineup = process_game_data(game_details, playing_lineup)

        conn, cursor = connect_to_games_database()
        create_games_tables(cursor)

        print("games details table created")


        game_id = load_game_details(cursor, df_game_details)
        conn.commit()
        print("loaded game details")

        if game_id > 0:

            # print(cursor.execute("SELECT * FROM game_details").fetchall())

            load_player_lineup(cursor, df_playing_lineup, game_id)
            conn.commit()
            print("loaded player lineup")
            # print(cursor.execute("SELECT * FROM player_lineup").fetchall())

            df_shot_data = read_shot_data(shot_data_path)
            create_shots_tables(cursor)
            print(game_id)
            load_shot_data(cursor, df_shot_data, game_id)
            conn.commit()
            # print(cursor.execute("SELECT * FROM shots_table LIMIT 5").fetchall())

        cursor.close()
        conn.close()
        move_file_to_processed_folder(game_data_path)
        move_file_to_processed_folder(shot_data_path)
        print("closed connection")


if __name__ == "__main__":
    run("../data/drop")
