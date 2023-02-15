import streamlit as st

def defaultConfig(pagesize:int=0) -> None:
    if pagesize == 0:
        st.set_page_config(layout="wide")
    elif pagesize == 1:
        st.set_page_config(layout="centered")
        
    hide_st_style = """
                <style>
                MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def process_image(image):
    # Add your image processing code here
    st.text("Your Uploaded Image")
    return st.image(image, use_column_width=True)