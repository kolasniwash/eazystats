import json
from enum import Enum
from dataclasses import dataclass
from typing import Optional


@dataclass(unsafe_hash=True)
class PlayingLineup:
    lead: str
    second: str
    third: str
    fourth: str
    skip: str
    vice: str
    alternate: str

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class ShotHandle(Enum):
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
    handle: ShotHandle
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

    def set_lineup(self, lineup):
        self.lineup = lineup

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
