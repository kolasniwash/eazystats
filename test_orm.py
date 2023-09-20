from datetime import datetime

import model
from sqlalchemy.sql import text, select


# def test_game_mapper_can_load_lines(session):
#
#     game1 = model.Game("Tallin", "2023", "2023-08-01", "Bice", 8, "R9")
#     game2 = model.Game("Tallin", "2023", "2023-08-02", "Miller", 8, "R12")
#
#     session.execute(text(
#         f'''INSERT INTO game_details (game_id, event_name, season, date, opponent, reg_ends, tournament_round ) VALUES
#         ({game1.game_id}, "Tallin", "2023", "2023-08-01", "Bice", 8, "R9"),
#         ({game2.game_id}, "Tallin", "2023", "2023-08-02", "Miller", 8, "R12")''')
#     )
#
#     expected = [
#         game1,
#         game2
#     ]
#     assert session.scalars(select(model.Game)).all() == expected


def test_player_lineup_can_load_lines(session):

    lineup1 = model.PlayingLineup('nico', 'edu', 'mikel', 'sergio', 'sergio', 'nico', 'luis')
    lineup2 = model.PlayingLineup('luis', 'edu', 'mikel', 'sergio', 'sergio', 'luis', 'nico')


    session.execute(text(
        f'''INSERT INTO player_lineup (lead, second, third, fourth, skip, vice, alternate) VALUES
        ('nico', 'edu', 'mikel', 'sergio', 'sergio', 'nico', 'luis'),
        ('luis', 'edu', 'mikel', 'sergio', 'sergio', 'luis', 'nico')''')
    )

    expected = [
        lineup1,
        lineup2
    ]
    assert session.scalars(select(model.PlayingLineup)).all() == expected

# def test_shotstats_mapper_can_load_lines(session):
#     session.execute(text(
#         '''INSERT INTO shot_stats (end, throw_in_end, shot_type, handle, difficulty, score, draw_or_hit, thrower_position) VALUES
#         (1, 1, "Center Guard", "OUT", 1, 4, "D", "lead"),
#         (1, 2, "Come Around", "IN", 1, 4, "D", "lead"),
#         (1, 3, "Open Hit", "OUT", 1, 4, "H", "second")''')
#     )
#
#     expected = [
#         model.ShotStat(1, 1, "Center Guard", "OUT", 1, 4, "D"),
#         model.ShotStat(1, 2, "Come Around", "IN", 1, 4, "D"),
#         model.ShotStat(1, 3, "Open Hit", "OUT", 1, 4, "H"),
#     ]
#     assert session.scalars(select(model.ShotStat)).all() == expected


def test_saving_game_detail(session):
    date = datetime.strptime("2023-08-01", "%Y-%m-%d").date()
    lineup = model.PlayingLineup('nico', 'edu', 'mikel', 'sergio', 'sergio', 'nico', 'luis')
    game = model.Game("Tallin", "2023", date, "Bice", 8, "R9")
    session.add(game)
    session.commit()
    rows = session.execute(
        text('SELECT event_name, season, date, opponent, reg_ends, tournament_round FROM game_details')
    )
    assert list(rows) == [("Tallin", "2023", "2023-08-01", "Bice", 8, "R9")]


def test_saving_player_lineup(session):
    date = datetime.strptime("2023-08-01", "%Y-%m-%d").date()
    lineup = model.PlayingLineup('nico', 'edu', 'mikel', 'sergio', 'sergio', 'nico', 'luis')
    session.add(lineup)
    session.commit()
    rows = session.execute(
        text('SELECT lead, second, third, fourth FROM player_lineup')
    )
    assert list(rows) == [('nico', 'edu', 'mikel', 'sergio',)]