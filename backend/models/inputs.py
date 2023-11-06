from typing import List, Optional
from pydantic import BaseModel

class GameInput(BaseModel):
    file: str
    our_score: int
    opponent_score: int
    opponent: str
    date: str
    game_result: str
    event_name: str
    season: str
    reg_ends: int
    tournament_stage: str
    lead: str
    second: str
    third: str
    fourth: str
    alternate: str
