import json
from enum import Enum
from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class PlayerPosition:
    lead: str
    second: str
    third: str
    fourth: str
    skip: str
    vice: str
    alternate: str


class ShotTurn(Enum):
    out_turn = "OUT"
    in_turn = "IN"


def throw_position_mapping():
    position_number_map = {
        1: "lead",
        2: "lead",
        3: "second",
        4: "second",
        5: "third",
        6: "third",
        7: "fourth",
        8: "fourth"
    }
    return position_number_map

@dataclass
class ShotStat:
    end: int
    throw_in_end: int
    shot_type: str
    turn: ShotTurn
    difficulty: int
    score: int
    draw_or_hit: str

    def __post_init__(self):
        mapping = throw_position_mapping()
        self.thrower_position = mapping[self.throw_in_end]


class Game:
    def __init__(self, event_name, season, date, opponent, reg_ends, tournament_round):
        self.event_name = event_name
        self.season = season
        self.date = date
        self.opponent = opponent
        self.reg_ends = reg_ends
        self.tournament_round = tournament_round
        self.game_id = hash(self)
        self.lineup = None
        self.shot_stats = OrderedDict()

    def set_lineup(self, lineup):
        self.lineup = lineup

    def add_shot_stat(self, shot_stat):
        if shot_stat.throw_in_end > 8:
            raise ValueError("Throw in end must be between 1 and 8")

        if shot_stat.end > self.reg_ends:
            raise ValueError("End must be between 1 and the number of regulation ends")

        self.shot_stats[(shot_stat.end, shot_stat.throw_in_end)] = shot_stat

    def __repr__(self):
        return f"<Game {self.game_id}>"

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        return other.game_id == self.game_id

    def __gt__(self, other):
        if self.date is None:
            return False
        if other.date is None:
            return True
        return self.date > other.date

    def __hash__(self):
        return hash((self.event_name, self.season, self.date, self.opponent, self.reg_ends, self.tournament_round))

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
