from collections import OrderedDict
from typing import Optional

from sqlalchemy import (Table,
                        MetaData,
                        Column,
                        Integer,
                        String,
                        Date,
                        ForeignKey,
                        UniqueConstraint)
from sqlalchemy.orm import relationship, registry, clear_mappers

mapper_registry = registry()

import model


metadata = MetaData()

game_details = Table(
    "game_details",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("game_id", String(255), nullable=False),
    Column("event_name", String(255), nullable=False),
    Column("season", String(255), nullable=False),
    Column("date", Date, nullable=False),
    Column("opponent", String(255), nullable=False),
    Column("reg_ends", Integer, nullable=False),
    Column("tournament_round", String(255), nullable=False),
    UniqueConstraint("event_name", "season", "opponent", "tournament_round")
)


player_lineup = Table(
    "player_lineup",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("lead", String(255)),
    Column("second", String(255)),
    Column("third", String(255)),
    Column("fourth", String(255)),
    Column("vice", String(255), nullable=False),
    Column("skip", String(255), nullable=False),
    Column("alternate", String(255))
)

# games = Table(
#     "games",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("game_id", ForeignKey("game_details.id")),
#     Column("lineup_id", ForeignKey("player_lineup.id")),
# )
# shot_stats = Table(
#     "shot_stats",
#     metadata,
#     Column("id", BIGINT, primary_key=True, autoincrement=True),
#     Column("end", Integer),
#     Column("throw_in_end", Integer),
#     Column("shot_type", String(255)),
#     Column("handle", String(255)),
#     Column("difficulty", Integer),
#     Column("score", Integer),
#     Column("draw_or_hit", String(255)),
#     Column("thrower_position", String(255)),
#     UniqueConstraint("id", "end", "throw_in_end")
# )


def start_mappers():
    clear_mappers()
    mapper_registry.map_imperatively(model.PlayingLineup, player_lineup)
    # mapper_registry.map_imperatively(model.ShotStat, shot_stats)
    mapper_registry.map_imperatively(model.Game, game_details)
