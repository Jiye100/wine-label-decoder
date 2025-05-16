# menu.py
import streamlit as st

def menu():
    st.sidebar.page_link("Home.py")
    st.sidebar.page_link("pages/1_Wine_Reader.py")
    st.sidebar.page_link("pages/2_Wine_Information.py")
