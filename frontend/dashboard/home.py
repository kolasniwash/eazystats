import json
from pandas import read_csv

import streamlit as st
import requests
from utils import get_events_list, _TEAM_LINEUPS, get_unique_players

_PLACEHOLDER_SELECT = "Choose option"
_PLACEHOLDER_FILL = "Please fill in"
_INPUT_DICT = dict()





st.title("Game Input Form")

# st.file_uploader("Local File CSV:")
# file_path = st.text_input("CSV File Path:", placeholder=_PLACEHOLDER_FILL)
input_file = st.file_uploader(label="File", type='csv')
st.title("Game Results")

# games 2 and 4: pablo, iñigo, eneko y carasa
# games 5, 6 and 7: iñigo, iraitz, eneko y carasa

def add_new_option(name_input, key):
    if name_input == "ADD NEW...":
        name_input = st.text_input("Enter new name...", key=key)
    return name_input

teams = list(_TEAM_LINEUPS.keys()) + ["ADD NEW..."]
team_name_input = st.selectbox("Select team", options=teams)
_INPUT_DICT["team"] = add_new_option(team_name_input, "team")
st.info(f"Team: {_INPUT_DICT['team']}")

_INPUT_DICT["our_score"] = st.text_input("Our Score:", placeholder=_PLACEHOLDER_FILL)
_INPUT_DICT["opponent_score"] = st.text_input("Opponent Score:", placeholder=_PLACEHOLDER_FILL)
_INPUT_DICT["opponent"] = st.text_input("Opponent Name:", placeholder=_PLACEHOLDER_FILL)
_INPUT_DICT["hammer"] = st.selectbox("Started game with Hammer:", options=["YES", "NO"])

_INPUT_DICT["date"] = st.date_input("Date:", value="today", format="YYYY-MM-DD").strftime("%Y-%m-%d")

_INPUT_DICT["game_result"] = st.selectbox(
    "Game result",
    ["Win", "Loss", "Tie"],
    placeholder=_PLACEHOLDER_SELECT
)

_INPUT_DICT["event_name"] = st.selectbox(
    "Event Name:",
    get_events_list(),
    placeholder=_PLACEHOLDER_SELECT
)

_INPUT_DICT["season"] = st.selectbox(
    "Season",
    ["2022-2023", "2023-2024"],
    placeholder=_PLACEHOLDER_SELECT
)

_INPUT_DICT["reg_ends"] = st.selectbox(
    "Regulation Ends",
    [8, 10],
    placeholder=_PLACEHOLDER_SELECT
)

_INPUT_DICT["tournament_stage"] = st.selectbox(
    "Tournament Stage",
    ["Round Robin", "Playoffs"],
    placeholder=_PLACEHOLDER_SELECT
)

st.title("Playing Positions:")
TEAM_PLAYERS = get_unique_players(team_name_input) if team_name_input in _TEAM_LINEUPS else []
_PLAYER_OPTIONS = TEAM_PLAYERS + ["ADD NEW..."]
st.info(f"Players: {_PLAYER_OPTIONS}")

lead_input = st.selectbox("Lead", options=_PLAYER_OPTIONS)
_INPUT_DICT["lead"] = add_new_option(lead_input, "lead")
st.info(f"lead: {_INPUT_DICT['lead']}")

second_input = st.selectbox("Second", options=_PLAYER_OPTIONS)
_INPUT_DICT["second"] = add_new_option(second_input, "second")
st.info(f"second: {_INPUT_DICT['second']}")

third_input = st.selectbox("Third", options=_PLAYER_OPTIONS)
_INPUT_DICT["third"] = add_new_option(third_input, "third")
st.info(f"third: {_INPUT_DICT['third']}")

fourth_input = st.selectbox("Fourth", options=_PLAYER_OPTIONS)
_INPUT_DICT["fourth"] = add_new_option(fourth_input, "fourth")
st.info(f"fourth: {_INPUT_DICT['fourth']}")

alternate_input = st.selectbox("Alternate", options=_PLAYER_OPTIONS)
_INPUT_DICT["alternate"] = add_new_option(alternate_input, "alternate")
st.info(f"alternate: {_INPUT_DICT['alternate']}")


if st.button("Submit"):
    st.info("Submit")
    st.info(_INPUT_DICT)

    df = read_csv(input_file)
    df = df[df["SCORE"] < 5]
    _INPUT_DICT['input_json'] = df.to_json(orient='records')

    r = requests.post("http://backend:8000/eazystats/v1/games/new",
                  data=json.dumps(_INPUT_DICT))
    st.info(r.status_code)
    if r.status_code == 200:
        st.success("Game successfully submitted!")

