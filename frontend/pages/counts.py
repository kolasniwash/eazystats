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