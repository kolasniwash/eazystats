import json
from datetime import datetime
from pandas import read_csv

import streamlit as st
import requests

_PLACEHOLDER_SELECT = "Choose option"
_PLACEHOLDER_FILL = "Please fill in"
_INPUT_DICT = dict()





st.title("Game Input Form")

# st.file_uploader("Local File CSV:")
# file_path = st.text_input("CSV File Path:", placeholder=_PLACEHOLDER_FILL)
input_file = st.file_uploader(label="File", type='csv')
st.title("Game Results")
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
    ["WCT Tallinn", "WCT Bern", "WCT Lodz"],
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
_PLAYERS = ["nico", "edu", "luis", "mikel", "sergio"]
_INPUT_DICT["lead"] = st.selectbox("Lead", _PLAYERS, placeholder="luis")
_INPUT_DICT["second"] = st.selectbox("Second", _PLAYERS, placeholder=_PLACEHOLDER_SELECT)
_INPUT_DICT["third"] = st.selectbox("Third", _PLAYERS, placeholder=_PLACEHOLDER_SELECT)
_INPUT_DICT["fourth"] = st.selectbox("Fourth", _PLAYERS, placeholder=_PLACEHOLDER_SELECT)
_INPUT_DICT["alternate"] = st.selectbox("Alternate", _PLAYERS, placeholder=_PLACEHOLDER_SELECT)


if st.button("Submit"):
    print("Submit")
    print(_INPUT_DICT)


    #read the input file in the frontend
    #convert to json
    #pass the json string to the backend with the other data
    #save the json data as record

    #### add started with hammer
    df = read_csv(input_file)
    _INPUT_DICT['input_json'] = df.to_json(orient='records')

    r = requests.post("http://backend:8000/eazystats/v1/games/new",
                  data=json.dumps(_INPUT_DICT))
    print(r.status_code)
    if r.status_code == 200:
        # filename = f"{_INPUT_DICT['event_name']}-{_INPUT_DICT['opponent']}-{datetime.now()}.json"
        # with open(f"~/data/raw/{filename}", 'w+') as json_file:
        #     json.dump(_INPUT_DICT, json_file)

        st.success("Game successfully submitted!")

