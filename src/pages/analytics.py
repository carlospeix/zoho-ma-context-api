import streamlit as st
import pandas as pd

def main():
    st.title("Analytics Page")
    st.write("Here you can display analytics and charts.")
    df = pd.DataFrame({"A": [1,2,3], "B": [4,5,6]})
    st.dataframe(df)

if __name__ == "__main__":
    main()
