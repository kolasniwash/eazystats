

def get_player_lineup_query():
    return """
        SELECT distinct team, position, player
        from game_details as g
        inner join player_lineup as pl
        on g.game_id = pl.game_id;
        """