def create_games_tables(cursor):
    """ Executes DDL statements and creates tables in the database """
    game_details_ddl = """
CREATE TABLE IF NOT EXISTS game_details (
    game_id SERIAL PRIMARY KEY,
    event_name VARCHAR(255),
    season VARCHAR(255),
    date DATE,
    opponent VARCHAR(255),
    reg_ends INTEGER,
    tournament_round VARCHAR(255),
    UNIQUE (event_name, season, opponent, tournament_round)
    );
    """
    cursor.execute(game_details_ddl)


def create_player_lineup_tables(cursor):
    player_lineup_ddl = """
CREATE TABLE IF NOT EXISTS player_lineup
(
    id       SERIAL PRIMARY KEY,
    game_id  INTEGER,
    position VARCHAR(255),
    player   VARCHAR(255),
    UNIQUE (game_id, position, player),
    FOREIGN KEY (game_id) REFERENCES game_details (game_id)
);
    """
    cursor.execute(player_lineup_ddl)


def create_shots_tables(cursor):
    create_shots_table_ddl = """
CREATE TABLE IF NOT EXISTS shots_table (
    shot_id SERIAL PRIMARY KEY,
    game_id INTEGER,
    end_num INTEGER,
    throw_in_end INTEGER,
    thrower_position VARCHAR(255),
    shot_type VARCHAR(255),
    turn VARCHAR(255),
    score INTEGER,
    UNIQUE (game_id, end_num, throw_in_end),
    FOREIGN KEY (game_id) REFERENCES game_details (game_id)
    );"""
    cursor.execute(create_shots_table_ddl)


def reset_all_entry_tables(cursor):
    cursor.execute("DROP TABLE player_lineup")
    cursor.execute("DROP TABLE shots_table")
    cursor.execute("DROP TABLE game_details")
