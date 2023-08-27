from model import Game, PlayerPosition, ShotStat, ShotTurn


def make_game():
    return Game(
        'WCT_test',
        '2023/24',
        '09/09/2023',
        'test opponent',
        8,
        'R2')

def test_adding_a_game():
    game = make_game()

    assert game.event_name == 'WCT_test'
    assert game.season == '2023/24'
    assert game.date == '09/09/2023'
    assert game.opponent == 'test opponent'
    assert game.reg_ends == 8
    assert game.tournament_round == 'R2'
    assert game.game_id == hash(Game('WCT_test', '2023/24', '09/09/2023', 'test opponent', 8, 'R2'))


def test_add_game_player_lineup():
    game = make_game()

    positions = PlayerPosition('nico', 'edu', 'mikel', 'sergio', 'sergio', 'nico', 'luis')
    game.set_lineup(positions)

    assert game.lineup == positions
    assert game.lineup.lead == 'nico'
    assert game.lineup.second == 'edu'


def test_create_shot_stat():
    shot = ShotStat(1, 1, 'draw', ShotTurn.in_turn, 1, 4, 'draw')

    assert shot.end == 1
    assert shot.throw_in_end == 1
    assert shot.thrower_position == 'lead'
    assert shot.shot_type == 'draw'
    assert shot.turn.value == "IN"
    assert shot.difficulty == 1
    assert shot.score == 4
    assert shot.draw_or_hit == 'draw'

    shot = ShotStat(1, 2, 'draw', ShotTurn.out_turn, 1, 4, 'draw')
    assert shot.thrower_position == 'lead'
    assert shot.turn.value == "OUT"

    shot = ShotStat(1, 3, 'draw', ShotTurn.out_turn, 1, 4, 'draw')
    assert shot.thrower_position == 'second'

    shot = ShotStat(1, 5, 'draw', ShotTurn.out_turn, 1, 4, 'draw')
    assert shot.thrower_position == 'third'

    shot = ShotStat(1, 7, 'draw', ShotTurn.out_turn, 1, 4, 'draw')
    assert shot.thrower_position == 'fourth'


def test_add_game_shot_stat():
    game = make_game()
    positions = PlayerPosition('nico', 'edu', 'mikel', 'sergio', 'sergio', 'nico', 'luis')

    shot1 = ShotStat(1, 1, 'draw', ShotTurn.out_turn, 1, 4, 'draw')
    shot2 = ShotStat(1, 2, 'draw', ShotTurn.in_turn, 2, 4, 'draw')
    shot3 = ShotStat(1, 3, 'hit', ShotTurn.out_turn, 2, 4, 'hit')
    shot4 = ShotStat(1, 4, 'draw', ShotTurn.in_turn, 3, 4, 'hit')

    game.add_shot_stat(shot1)
    game.add_shot_stat(shot2)
    game.add_shot_stat(shot3)
    game.add_shot_stat(shot4)
    game.add_shot_stat(shot4)

    assert len(game.shot_stats) == 4
    assert game.shot_stats[(1, 1)] == shot1
    assert game.shot_stats[(1, 2)] == shot2
    assert game.shot_stats[(1, 3)] == shot3
    assert game.shot_stats[(1, 4)] == shot4
