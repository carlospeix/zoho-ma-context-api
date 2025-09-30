import streamlit as st
from pages import home, analytics, zoho_widget_examples

st.set_page_config(page_title="Streamlit Multi-Page App", layout="wide")

PAGES = {
    "Home": home,
    "Analytics": analytics,
    "Zoho Widget Examples": zoho_widget_examples,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.render()
