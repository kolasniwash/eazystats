

def insert_into_game_details_query(**kwargs):
    # Write the dataframes to SQLite tables
    return f"""INSERT INTO game_details (
        event_name, 
        season, 
        date,
        opponent,
        reg_ends,
        tournament_round) 
        VALUES (
        '{kwargs['event_name']}',
        '{kwargs['season']}',
        '{kwargs['date']}',
        '{kwargs['opponent']}',
        '{kwargs['reg_ends']}',
        '{kwargs['tournament_round']}')
        ON CONFLICT (event_name, season, opponent, tournament_round) DO NOTHING;"""
    # cursor.execute(insert_game_details_ddl, tuple(df_game_details.values[0]))


def insert_into_player_lineup_query(game_id, **kwargs):
    return f"""
    INSERT INTO player_lineup (
    game_id, lead, second, third, fourth, vice, skip, alternate)
    VALUES (
    '{game_id}',
    '{kwargs['lead']}',
    '{kwargs['second']}',
    '{kwargs['third']}',
    '{kwargs['fourth']}',
    '{kwargs['vice']}',
    '{kwargs['skip']}',
    '{kwargs['alternate']}');"""

    # player_lineup_values = df_playing_lineup.values.tolist()[0]
    # player_lineup_values.insert(0, game_id)
    # cursor.execute(insert_player_lineup_ddl, tuple(player_lineup_values))


def create_games_tables(cursor):
    """ Executes DDL statements and creates tables in the database """
    game_details_ddl = """
    CREATE TABLE IF NOT EXISTS game_details (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    cursor.execute(player_lineup_ddl)


def reset_all_entry_tables(cursor):
    cursor.execute("DROP TABLE IF EXISTS game_details")
    cursor.execute("DROP TABLE IF EXISTS player_lineup")
