import pandas as pd
from fastapi import APIRouter, Request
from backend.db import get_postgres_connection
from backend.query.aggregates import (
    get_shot_counts_query,
    get_player_averages_query,
    get_shot_type_counts
)

router = APIRouter(
    prefix="/views",
    tags=["views"],
)

@router.get("/shot_counts")
async def shot_counts_data(request: Request):

    kwargs = request.query_params
    query = get_shot_counts_query(**kwargs)
    print(query)
    with get_postgres_connection() as conn:
        shot_counts = pd.read_sql(query, conn)

    shot_counts = shot_counts.set_index("player").astype(int)
    shot_count_norm = shot_counts.div(shot_counts.sum(axis=1), axis=0) * 100

    return {"data": shot_count_norm.to_json()}



@router.get("/player_averages")
async def summary_data(request: Request):

    kwargs = request.query_params
    query = get_player_averages_query(**kwargs)

    with get_postgres_connection() as conn:
        player_avg = pd.read_sql(query, conn)

    return {"data": player_avg.to_json()}


@router.get("/shot_types")
async def shot_types(request: Request):
    kwargs = request.query_params
    query = get_shot_type_counts(**kwargs)

    with get_postgres_connection() as conn:
        player_avg = pd.read_sql(query, conn)

    return {"data": player_avg.to_json()}