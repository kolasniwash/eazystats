INSERT INTO statistics (
WITH previous_stats AS (
    SELECT * FROM statistics
    WHERE game_id =20
),
    current_game AS (
        SELECT * FROM game_details
        WHERE game_id = 21
    ),
    current_game_stats AS (
        SELECT
            cg.game_id AS game_id,
            CASE WHEN pl.position = 'alternate' THEN NULL ELSE
                ROW(
                    AVG(score),
                    COUNT(1),
                    SUM(score),
                    COUNT(1) FILTER (WHERE turn = 'IN'),
                    SUM(score) FILTER (WHERE turn = 'IN'),
                    COUNT(1) FILTER (WHERE turn = 'OUT'),
                    SUM(score) FILTER (WHERE turn = 'OUT')
                    )::stats
            END AS performance,
            CASE WHEN pl.position = 'alternate' THEN NULL ELSE
                ROW(
                    COUNT(1) FILTER (WHERE st.score = 4),
                    COUNT(1) FILTER (WHERE st.score = 3),
                    COUNT(1) FILTER (WHERE st.score = 2),
                    COUNT(1) FILTER (WHERE st.score = 1),
                    COUNT(1) FILTER (WHERE st.score = 0),
                    COUNT(1)
                    )::shots
            END as shot_counts,
            pl.position::positions as position,
            pl.player::players AS player,
            event_name::events AS event,
            season::seasons as season,
            CASE WHEN pl.position = 'alternate' THEN FALSE ELSE TRUE END AS played_game
        FROM current_game AS cg
        JOIN player_lineup AS pl on pl.game_id = cg.game_id
        LEFT JOIN shots_table AS st ON cg.game_id = st.game_id
            AND st.thrower_position = pl.position
        GROUP BY cg.game_id, pl.position, player, event_name, season, played_game
    )
SELECT
    COALESCE(cgs.game_id, ps.game_id) as game_id,
    COALESCE(cgs.position, 'alternate') as poisition,
    COALESCE(cgs.player, ps.player) as player,
    CASE
        WHEN cgs.position = 'alternate' THEN ps.games
        WHEN ps.games IS NULL THEN
            ARRAY[
                ROW(
                    cgs.performance,
                    cgs.shot_counts
                        )::games]
        ELSE (
            ps.games || ARRAY[
                ROW(
                    cgs.performance,
                    cgs.shot_counts
                    )::games]
            )
        END as games,
    COALESCE(cgs.performance, NULL) as performance,
    COALESCE(cgs.shot_counts, NULL) as shot_counts,
    COALESCE(cgs.event, ps.event) as event,
    COALESCE(cgs.season, ps.season) as season,
    cgs.played_game
FROM current_game_stats AS cgs
FULL OUTER JOIN previous_stats AS ps
    ON cgs.player = ps.player);