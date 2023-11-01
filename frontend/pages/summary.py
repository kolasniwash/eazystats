import json

import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

st.title("Summary")


def get_summary_data(event, playing_lineup):
    response = requests.get(
        "http://127.0.0.1:8000/eazystats/v1/summary/data",
        params={"event": event, **playing_lineup}
    )
    print(response)
    return pd.read_json(response.json()["data"])

def get_available_events_list():
    return ["ALL", "WCT Bern", "WCT Tallinn"]

selected_event = st.selectbox(
    "Select Event",
    get_available_events_list()
)

lineup = {
    "lead": "nico",
    "second": "edu",
    "third": "mikel",
    "fourth": "sergio"
}

player_avg = get_summary_data(event="WCT Bern", playing_lineup=lineup)

# if selected_event != 'ALL':
#     player_avg = player_avg[player_avg['event'] == selected_event]
#
# player_avg = player_avg.drop(columns=['event'])


fig, axes = plt.subplots(1, 1, figsize=(6,3))
view_averages = player_avg.pivot(columns='player', values='average')
ax_averages = view_averages.plot(kind='box', ax=axes, fontsize=7)

# Customize the chart (optional)
ax_averages.set_title('Range of game scoring averages', fontsize=7)
ax_averages.set_xlabel('Player', fontsize=7)
ax_averages.set_ylabel('Score', fontsize=7)
ax_averages.set_yticks(range(0, 5))

st.pyplot(fig)


fig, axes = plt.subplots(1, 2, figsize=(6, 3))
view_out = player_avg.pivot(columns='player', values='out_average')
ax_out = view_out.plot(kind='box', ax=axes[0], widths=0.5, fontsize=7)

# Customize the chart (optional)
ax_out.set_title('Averages - OUT TURN', fontsize=7)
ax_out.set_xlabel('Player', fontsize=7)
ax_out.set_ylabel('Score', fontsize=7)
ax_out.set_yticks(range(0, 5))

view_in = player_avg.pivot(columns='player', values='in_average')
ax_in = view_in.plot(kind='box', ax=axes[1], widths=0.5, fontsize=7)
ax_in.set_title('Averages - IN TURN', fontsize=7)
ax_in.set_xlabel('Player', fontsize=7)
ax_in.set_ylabel('Score', fontsize=7)
ax_in.set_yticks(range(0, 5))

st.pyplot(fig)