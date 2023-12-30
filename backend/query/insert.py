def insert_into_game_details_query(**kwargs):
    # Write the dataframes to SQLite tables
    return f"""INSERT INTO game_details (
        event_name, 
        season, 
        date,
        opponent,
        reg_ends,
        tournament_round,
        hammer,
        result,
        our_score,
        opponent_score) 
        VALUES (
        '{kwargs['event_name']}',
        '{kwargs['season']}',
        '{kwargs['date']}',
        '{kwargs['opponent']}',
        '{kwargs['reg_ends']}',
        '{kwargs['tournament_stage']}',
        '{kwargs['hammer']}',
        '{kwargs['game_result']}',
        '{kwargs['our_score']}',
        '{kwargs['opponent_score']}')
        ON CONFLICT (event_name, season, opponent, tournament_round) DO NOTHING
        RETURNING game_id;"""


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
