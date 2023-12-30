import streamlit as st


_PLAYERS = ["luis", 'edu', 'sergio', 'mikel', 'nico']

st.title("Performance Summary")

st.header("Season Summary")

stats = {
    "hammer_eff": 0.5,
    "steal_eff": 0.5,
    "force_eff": 0.5,
    "steal_def": 0.5,
    "big_end_per_game": 0.5,
    "points_for_per_game": 0.5,
    "points_against_per_game": 0.5
}

col1, col2, col3 = st.columns(3)

with col1:
    st.text("Wins: X")
    st.text("Losses: X")

with col2:
    st.text(f"Hammer Efficiency: {stats['hammer_eff']}")
    st.text(f"Steal Efficiency: {stats['steal_eff']}")
    st.text(f"Force Efficiency: {stats['force_eff']}")
    st.text(f"Steal Defence: {stats['steal_def']}")

with col3:
    st.text(f"Big Ends / Game: {stats['big_end_per_game']}")
    st.text(f"Points Score / Game: {stats['points_for_per_game']}")
    st.text(f"Points Given / Game: {stats['points_against_per_game']}")

st.header("Throwing Average")

query_averages = {
    "luis": 0.5,
    'edu': 0.5,
    "sergio": 0.5,
    "mikel": 0.5,
    "nico": 0.5
}
cols = st.columns(5)
for col, (player, average) in zip(cols, query_averages.items()):
    with st.container():
        col.text(player)
        col.text(average)

st.header("Made After Miss")

query_made_after_miss = {
    "luis": 0.5,
    'edu': 0.5,
    "sergio": 0.5,
    "mikel": 0.5,
    "nico": 0.5
}

cols = st.columns(5)
for col, (player, mam) in zip(cols, query_made_after_miss.items()):
    with st.container():
        col.text(player)
        col.text(mam)
