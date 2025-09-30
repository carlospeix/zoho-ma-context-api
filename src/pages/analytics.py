import streamlit as st
import pandas as pd

def render():
    st.title("Analytics Page")
    st.write("Here you can display analytics and charts.")
    df = pd.DataFrame({"A": [1,2,3], "B": [4,5,6]})
    st.dataframe(df)
