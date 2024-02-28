import requests
from typing import List, Dict
def get_events_list() -> List[str]:
    return ["WCT Tallinn", "WCT Bern", "WCT Lodz", "Bonspiel CHP", "CE MASCULINO"]


def get_teams(team_lineups) -> List[str]:
    return team_lineups.keys()


def get_team_lineups() -> Dict:
    request = requests.get(
        "http://backend:8000/eazystats/v1/players/lineups",
    )
    return request.json()["data"]

def get_unique_players(team) -> List[str]:
    unique_players = set()
    if team not in _TEAM_LINEUPS:
        return []

    for position in _TEAM_LINEUPS[team]:
        unique_players.update(_TEAM_LINEUPS[team][position])

    return list(unique_players)

_TEAM_LINEUPS = get_team_lineups()

