import load
import sqlite3
import pandas as pd
import datapane as dp



def run_query(query, db):
    with sqlite3.connect(db) as conn:
        return pd.read_sql(query, conn)

position_stats_query = """
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


position_breakdown_stats_query = """
        SELECT
            thrower_position as Position,
            ROUND(AVG(score) filter (where draw_or_hit = 'D' and turn = 'IN') * 100 / 4, 2)  AS 'In Turn Draws',
            ROUND(AVG(score) filter (where draw_or_hit = 'H' and turn = 'IN') * 100 / 4, 2)  AS 'In Turn Hits',
            ROUND(AVG(score) filter (where draw_or_hit = 'D' and turn = 'OUT') * 100 / 4, 2)  AS 'Out Turn Draws',
            ROUND(AVG(score) filter (where draw_or_hit = 'H' and turn = 'OUT') * 100 / 4, 2)  AS 'Out Turn Hits',
            ROUND(AVG(score) filter (where draw_or_hit = 'D') * 100 / 4, 2)  AS 'Total Draws',
            ROUND(AVG(score) filter (where draw_or_hit = 'H') * 100 / 4, 2)  AS 'Total Hits'
        FROM shots_table
        GROUP BY thrower_position;
"""

player_breakdown_stats_query = """
        SELECT
            thrower_name as Player,
            ROUND(AVG(score) filter (where draw_or_hit = 'D' and turn = 'IN') * 100 / 4, 2)  AS 'In Turn Draws',
            ROUND(AVG(score) filter (where draw_or_hit = 'H' and turn = 'IN') * 100 / 4, 2)  AS 'In Turn Hits',
            ROUND(AVG(score) filter (where draw_or_hit = 'D' and turn = 'OUT') * 100 / 4, 2)  AS 'Out Turn Draws',
            ROUND(AVG(score) filter (where draw_or_hit = 'H' and turn = 'OUT') * 100 / 4, 2)  AS 'Out Turn Hits',
            ROUND(AVG(score) filter (where draw_or_hit = 'D') * 100 / 4, 2)  AS 'Total Draws',
            ROUND(AVG(score) filter (where draw_or_hit = 'H') * 100 / 4, 2)  AS 'Total Hits'
        FROM shots_table
        GROUP BY thrower_name;
"""


if __name__ == "__main__":
    # load.run()
    db = './data/db/games_data_test.db'
    con = sqlite3.connect('./data/db/games_data_test.db')

    print(run_query("SELECT * FROM game_details", db))
    print(run_query("SELECT * FROM player_lineup", db))
    print(run_query("SELECT * FROM shots_table LIMIT 1", db))

    position_stats = run_query(position_stats_query, db)
    position_breakdown_stats = run_query(position_breakdown_stats_query, db)
    player_breakdown_stats = run_query(player_breakdown_stats_query, db)

    view = dp.Group(
        blocks=[
        # dp.Text("Team Position Stats"),
        dp.DataTable(position_stats, label="Game Summaries by Position"),
        # dp.Text("Team Stats"),
        dp.Select(
            blocks=[
                dp.DataTable(position_breakdown_stats, label="Position by Turn and Shot Type"),
                dp.DataTable(player_breakdown_stats, label="Player by Turn and Shot Type"),
            ]
        )]
    )
    dp.save_report(view, path="./reports/index.html")
    dp.serve_app(view)
