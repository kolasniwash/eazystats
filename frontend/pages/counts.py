import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_shot_count_data():
    response = requests.get("http://127.0.0.1:8000/eazystats/v1/shot_counts/data")
    return pd.read_json(response.json()["data"])


st.title("Counts")

data = get_shot_count_data()
st.table(data)


st.bar_chart(
    data=data,
    x=None,
    y=["zero", "one", "two", "three", "four"],
    use_container_width=True
)




# fig, ax = plt.subplots(1, 1, figsize=(6, 3))

# ax = shot_count_norm.plot.bar(stacked=True, figsize=(3, 2), legend=False, fontsize=7)
# ax[1] = shot_counts.plot.bar(stacked=True, figsize=(3, 2), legend=False, secondary_y=True, ax=ax, fontsize=7)
# ax.legend(title="Scores", fontsize=7, loc='upper left', bbox_to_anchor=(1.2, 1))
# ax.set_title("How to make more 3s and 4s?", fontsize=7)
# ax.set_xlabel("Player name", fontsize=7)
# ax.set_ylabel("% Shots", fontsize=7)
# ax_counts.set_ylabel("No. Shots", fontsize=7)

# for bar in ax_counts.patches:
#     bar.set_facecolor('none')

# st.pyplot(fig)