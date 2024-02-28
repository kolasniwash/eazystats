import pandas as pd
from fastapi import APIRouter, Request
from backend.db import get_postgres_connection
from backend.query.players import get_player_lineup_query
from collections import defaultdict

router = APIRouter(
    prefix="/players",
    tags=["players"],
)


@router.get("/lineups")
async def summary_data(request: Request):

    kwargs = request.query_params
    query = get_player_lineup_query(**kwargs)

    with get_postgres_connection() as conn:
        lineups = pd.read_sql(query, conn)


    team_lineups = dict()

    for (idx, row) in lineups.iterrows():
        if row.team not in team_lineups:
            team_lineups[row.team] = defaultdict(list)

        if row.player not in team_lineups[row.team][row.position]:
            team_lineups[row.team][row.position].append(row.player)

    return {"data": team_lineups}
