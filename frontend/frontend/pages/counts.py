import streamlit as st
import requests
import pandas as pd

_PLAYERS = ["nico", "edu", "luis", "sergio", "mikel"]

def get_shot_count_data(event, playing_lineup, last_n_games):
    response = requests.get(
        "http://backend:8000/eazystats/v1/views/shot_counts",
        params={
            "event": event,
            **playing_lineup,
            "last_n_games": last_n_games
        }
    )
    print(response)
    return pd.read_json(response.json()["data"])

st.title("Counts")

def get_available_events_list():
    return ["WCT Bern", "WCT Tallinn", "WCT Lodz"]

last_n_games = st.select_slider(
    label="Select Number of games to include:",
    options=[i for i in range(1, 21)],
    value=7
)

event = st.sidebar.selectbox(
    "Select Event",
    get_available_events_list(),
    index=None
)

lead = st.sidebar.selectbox(
    "Lead:",
    _PLAYERS,
    index=None
)

second = st.sidebar.selectbox(
    "Second:",
    _PLAYERS,
    index=None
)

third = st.sidebar.selectbox(
    "Third:",
    _PLAYERS,
    index=None
)

fourth = st.sidebar.selectbox(
    "Fourth:",
    _PLAYERS,
    index=None
)

lineup = {
    "lead": lead,
    "second": second,
    "third": third,
    "fourth": fourth
}

data = get_shot_count_data(
    event=event,
    playing_lineup=lineup,
    last_n_games=last_n_games
)


st.bar_chart(
    data=data,
    x=None,
    y=["zero", "one", "two", "three", "four"],
    use_container_width=True
)

st.table(data)