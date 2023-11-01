from typing import List, Optional
from pydantic import BaseModel

class Choice(BaseModel):
    id: str
    label: str
    ref: str

class Field(BaseModel):
    id: str
    type: str
    ref: str

class Ending(BaseModel):
    id: str
    ref: str

class Answer(BaseModel):
    type: str
    choice: Optional[Choice] = None
    date: Optional[str] = None
    text: Optional[str] = None
    field: Field

class FormDefinition(BaseModel):
    id: str
    title: str
    fields: List[Field]
    endings: List[Ending]

class FormResponse(BaseModel):
    form_id: str
    token: str
    landed_at: str
    submitted_at: str
    definition: FormDefinition
    answers: List[Answer]
    ending: Ending

class TypeFormResponse(BaseModel):
    event_id: str
    event_type: str
    form_response: FormResponse


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

