def get_shot_counts_query(**kwargs):

    positions = list()
    for key, val in kwargs.items():
        if key == 'event':
            event_filter = f"AND event = '{val}'"

        if key in ('lead', 'second', 'third', 'fourth'):
            if val is None:
                continue
            positions.append(f"(position = '{key}' AND player = '{val}')")

    query = """
        SELECT
            player,
            SUM((shot_counts::shots).zero) as zero,
            SUM((shot_counts::shots).one) as one,
            SUM((shot_counts::shots).two) as two,
            SUM((shot_counts::shots).three) as three,
            SUM((shot_counts::shots).four) as four
        FROM statistics
        WHERE shot_counts is not null
            AND game_id BETWEEN 0 and {last_n_games}
            {event_filter} {playing_lineup_filter}
        GROUP BY player;
    """

    return query.format(
        event_filter="" if 'event' not in kwargs.keys() else event_filter,
        playing_lineup_filter="AND " + " OR ".join(positions) if len(positions) > 0 else "",
        last_n_games=kwargs.get("last_n_games", 1)
    )


def get_player_averages_query(**kwargs):

    positions = list()
    for key, val in kwargs.items():
        if key == 'event':
            event_filter = f"AND event = '{val}'"

        if key in ('lead', 'second', 'third', 'fourth'):
            if val is None:
                continue
            positions.append(f"(position = '{key}' AND player = '{val}')")


    query = """
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
    WHERE game_id BETWEEN 0 and {last_n_games}
        AND played_game
        {event_filter} {playing_lineup_filter};"""

    return query.format(
        event_filter="" if 'event' not in kwargs.keys() else event_filter,
        playing_lineup_filter="AND " + " OR ".join(positions) if len(positions) > 0 else "",
        last_n_games=kwargs.get("last_n_games", 1)
    )
