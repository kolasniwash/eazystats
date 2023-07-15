import sqlite3
import pandas as pd

def read_game_data():
    # Define the lists to store the game details and playing lineup
    game_details = []
    playing_lineup = []
    # Define the flag to check the current section
    in_game_details = False
    in_playing_lineup = False

    # Open the CSV file and iterate over lines
    with open('./data/drop/GameDataInputSample.csv') as file:
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

def read_shot_data():
    df_shot_data = pd.read_csv('./data/drop/ShotDataInputSample.csv')
    df_shot_data.dropna(inplace=True, subset="shot_type")
    print(df_shot_data.columns)
    return df_shot_data


def process_game_data(game_details, playing_lineup):
    # Convert the lists to dataframes
    df_game_details = pd.DataFrame(game_details[1:], columns=game_details[0])
    df_playing_lineup = pd.DataFrame(playing_lineup[1:], columns=playing_lineup[0])

    return df_game_details, df_playing_lineup


def connect_to_games_database():
    conn = sqlite3.connect('./data/db/games_data_test.db')
    cursor = conn.cursor()
    return cursor


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

    cursor.execute("DROP TABLE IF EXISTS game_details")
    cursor.execute(game_details_ddl)

    cursor.execute("DROP TABLE IF EXISTS player_lineup")
    cursor.execute(player_lineup_ddl)

def create_shots_tables(cursor):
    create_shots_table_ddl = """
    CREATE TABLE IF NOT EXISTS shots_table (
    shot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    end INTEGER,
    throw_in_end INTEGER,
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

    cursor.execute("DROP TABLE IF EXISTS shots_table")
    cursor.execute(create_shots_table_ddl)

def load_game_details(cursor, df_game_details):
    # Write the dataframes to SQLite tables
    insert_game_details_ddl = """INSERT INTO game_details (
        event_name, season, date, opponent, type, total_ends, stage) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (event_name, season, opponent, stage) DO NOTHING;"""
    cursor.execute(insert_game_details_ddl, tuple(df_game_details.values[0]))
    print("last row id ", cursor.lastrowid)
    return cursor.lastrowid

def load_player_lineup(cursor, df_playing_lineup, game_id):
    insert_player_lineup_ddl = """
    INSERT INTO player_lineup (
    game_id, lead, second, third, fourth, vice, skip, alternate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
    print("game id", game_id)
    player_lineup_values = df_playing_lineup.values.tolist()[0]
    player_lineup_values.insert(0, game_id)
    print("modified playing line up ", player_lineup_values)
    cursor.execute(insert_player_lineup_ddl, tuple(player_lineup_values))


def load_shot_data(cursor, df_shot_data, game_id):
    insert_shot_data_ddl = """
    INSERT INTO shots_table (
    game_id, end, throw_in_end, shot_type, 
    turn, difficulty, score, execution, line, 
    release_direction, release_rotation, speed, 
    sweeping, cleaning, sweeping_infraction, 
    thrower_stability, ice_given, draw_or_hit)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""


    for item in df_shot_data.values.tolist():
        item.insert(0, game_id)
        print("item ", item)
        cursor.execute(insert_shot_data_ddl, item)


if __name__ == "__main__":

    game_details, playing_lineup = read_game_data()
    df_game_details, df_playing_lineup = process_game_data(game_details, playing_lineup)

    cursor = connect_to_games_database()
    create_games_tables(cursor)
    #
    # cursor = conn.execute("PRAGMA table_info(game_details)")
    # schema = cursor.fetchall()
    # for column in schema:
    #     column_name = column[1]
    #     data_type = column[2]
    #     is_nullable = "NOT NULL" if column[3] == 1 else "NULL"
    #     default_value = column[4]
    #     is_primary_key = "PRIMARY KEY" if column[5] == 1 else ""
    #     print(f"{column_name}: {data_type} {is_nullable} {default_value} {is_primary_key}")

    print("games details table created")
    # Display the first few rows of the dataframes
    # print("game_details")
    # print(df_game_details.head())
    #
    # print("playing_lineup")
    # print(df_playing_lineup.head())

    game_id = load_game_details(cursor, df_game_details)
    print(cursor.execute("SELECT * FROM game_details").fetchall())
    print("loaded game details")
    load_player_lineup(cursor, df_playing_lineup, game_id)
    print(cursor.execute("SELECT * FROM player_lineup").fetchall())
    print("loaded player lineup")


    df_shot_data = read_shot_data()
    create_shots_tables(cursor)
    load_shot_data(cursor, df_shot_data, game_id)
    print(cursor.execute("SELECT * FROM shots_table LIMIT 5").fetchall())

    cursor.close()
    print("closed connection")

