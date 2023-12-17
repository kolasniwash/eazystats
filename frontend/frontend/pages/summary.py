import json
import altair as alt
import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd


_PLAYERS = ["nico", "edu", "luis", "sergio", "mikel"]

st.title("Summary")

def get_summary_data(event, playing_lineup, last_n_games):
    response = requests.get(
        "http://backend:8000/eazystats/v1/views/player_averages",
        params={
            "event": event,
            **playing_lineup,
            "last_n_games": last_n_games
        }
    )
    print(response)
    return pd.read_json(response.json()["data"])

def get_available_events_list():
    return ["WCT Bern", "WCT Tallinn", "WCT Lodz"]

last_n_games = st.select_slider(
    label="Select Number of games to include:",
    options=[i for i in range(1, 51)],
    value=50
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

player_avg = get_summary_data(
    event=event,
    playing_lineup=lineup,
    last_n_games=last_n_games
)

scatter_view = st.toggle("View as scatter plot", value=True)

if scatter_view:
    scatter_plot = alt.Chart(player_avg).mark_circle().encode(
        y=alt.Y('average', scale=alt.Scale(domain=[0, 4], clamp=False)),
        x=alt.X('player')
    )

    st.altair_chart(scatter_plot, use_container_width=True)

    scatter_plot_inturn = alt.Chart(player_avg).mark_circle().encode(
        y=alt.Y('in_average', scale=alt.Scale(domain=[0, 4], clamp=True)),
        x=alt.X('player')
    )
    scatter_plot_outturn = alt.Chart(player_avg).mark_circle().encode(
        y=alt.Y('out_average', scale=alt.Scale(domain=[0, 4], clamp=True)),
        x=alt.X('player')
    )
    st.altair_chart(scatter_plot_inturn)

    st.altair_chart(scatter_plot_outturn)
else:

    fig, axes = plt.subplots(1, 1, figsize=(6, 3))
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
