

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
        '{kwargs['tournament_stage']}')
        ON CONFLICT (event_name, season, opponent, tournament_round) DO NOTHING
        RETURNING game_id;"""
    # cursor.execute(insert_game_details_ddl, tuple(df_game_details.values[0]))


def insert_into_player_lineup_query(game_id, position, player):
    return f"""
    INSERT INTO player_lineup (
    game_id, position, player)
    VALUES (
    '{game_id}',
    '{position}',
    '{player}')
    ON CONFLICT (game_id, position, player) DO NOTHING;"""

    # player_lineup_values = df_playing_lineup.values.tolist()[0]
    # player_lineup_values.insert(0, game_id)
    # cursor.execute(insert_player_lineup_ddl, tuple(player_lineup_values))

def insert_shot_data_ddl(items):
    return f"""
    INSERT INTO shots_table (
    game_id, 
    end_num, 
    throw_in_end, 
    thrower_position,
    shot_type, 
    turn, 
    score)
    VALUES (
    {items['game_id']}, 
    {items['END']},
    {items['THROW IN END']},
    '{items['THROWER POSITION']}',
    '{items['SHOT TYPE']}',
    '{items['TURN']}',
    {items['SCORE']});"""


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


def aggregate_position_stats_query():
    return """
            WITH game_aggregates AS (
            SELECT
                game_id,
                ROUND(AVG(score) filter (where thrower_position = 'lead') * 100 / 4, 2)  AS lead,
                ROUND(AVG(score) filter (where thrower_position = 'second') * 100 / 4, 2)  AS second,
                ROUND(AVG(score) filter (where thrower_position = 'third') * 100 / 4, 2)  AS third,
                ROUND(AVG(score) filter (where thrower_position = 'fourth') * 100 / 4, 2)  AS fourth,
                ROUND(AVG(score)*100 / 4, 1) AS team_pct
            FROM shots_table
            GROUP BY game_id
            )
            SELECT
                gd.event_name,
                gd.opponent,
                ga.lead,
                ga.second,
                ga.third,
                ga.fourth,
                ga.team_pct
            FROM game_aggregates AS ga
            LEFT JOIN game_details AS gd ON ga.game_id = gd.game_id;"""

def number_of_zeros_per_player():
    return """
    with zero_counts as (
        select thrower_position, sum(CASE WHEN score = 0 THEN 1 ELSE 0 END) as num_zeros, count(*) as num_throws from shots_table group by thrower_position
    )
    select thrower_position,
        num_zeros,
        num_throws,
        (num_zeros / num_throws) * 100 as pct_zeros
        from zero_counts;"""

def histogram_lookback_query():
    pass

def get_player_position_histogram():
    return """
    SELECT
        thrower_position,
        sum(1) filter (where score = 0) as no_zero,
        sum(1) filter (where score = 1) as no_one,
        sum(1) filter (where score = 2) as no_two,
        sum(1) filter (where score = 3) as no_three,
        sum(1) filter (where score = 4) as no_four,
        ROUND(sum(1) filter (where score = 0) * 100 / count(*), 2)  AS pct_zero,
        ROUND(sum(1) filter (where score = 1) * 100 / count(*), 2)  AS pct_one,
        ROUND(sum(1) filter (where score = 2) * 100 / count(*), 2)  AS pct_two,
        ROUND(sum(1) filter (where score = 3) * 100 / count(*), 2)  AS pct_three,
        ROUND(sum(1) filter (where score = 4) * 100 / count(*), 2)  AS pct_four
    FROM shots_table
    WHERE shot_type is not null
    GROUP BY thrower_position;"""

def player_name_histogram():
    pass


def game_summary_query():
    return """
    SELECT 
        gd.season,
        gd.event_name,
        gd.opponent,
        st.thrower_position,
        CASE WHEN (thrower_position = 'lead') THEN pl.lead
            WHEN (thrower_position = 'second') THEN pl.second
            WHEN (thrower_position = 'third') THEN pl.third
            WHEN (thrower_position = 'fourth') THEN pl.fourth
            ELSE 'unknown' END as player_name,
        AVG(st.score) as total_pct, 
        AVG(st.score) filter (where turn  = 'OUT') as out_pct, 
        AVG(st.score) filter (where turn = 'IN') as in_pct, 
        sum(1) filter (where st.score=0) as no_zeros 
    FROM shots_table AS st
    LEFT JOIN player_lineup as pl ON st.game_id = pl.game_id
    LEFT JOIN game_details as gd ON st.game_id = gd.game_id
    WHERE shot_type is not null 
    GROUP BY st.game_id, st.thrower_position;"""


def get_shot_counts_query():
    return """
        SELECT
            player,
            SUM((shot_counts::shots).zero) as zero,
            SUM((shot_counts::shots).one) as one,
            SUM((shot_counts::shots).two) as two,
            SUM((shot_counts::shots).three) as three,
            SUM((shot_counts::shots).four) as four
        FROM statistics
        WHERE shot_counts is not null
            AND game_id BETWEEN 0 AND 3
        GROUP BY player;
    """

def get_player_averages_query():
    return """
    SELECT game_id,
       player,
       (performance::stats).average,
        (performance::stats).shot_count,
        (performance::stats).shot_total,
        (performance::stats).in_count,
        (performance::stats).in_total,
        (performance::stats).in_total / CAST((performance::stats).in_count AS real) as in_average,
        (performance::stats).out_count,
        (performance::stats).out_total,
        (performance::stats).out_total / CAST((performance::stats).out_count AS real) as out_average
    FROM statistics
    WHERE game_id BETWEEN 0 and 3
        AND position <> 'alternate';"""