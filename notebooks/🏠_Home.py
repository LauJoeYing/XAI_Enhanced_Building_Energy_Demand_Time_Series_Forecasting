import streamlit as st
from pathlib import Path

# Load custom CSS
base_path = Path(__file__).parent
stylesheet_file_path = (base_path / "./stylesheets/style.css").resolve()
with open(stylesheet_file_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 class='custom-title'>Welcome to Joe Ying's FYP</h1>", unsafe_allow_html=True)

# 1st step: upload the gif to gdrive
# 2nd step: share the file to public with "Anyone with the link" general access
# 3rd step: copy link
# 4th step: paste the link here: https://drive.google.com/file/d/1oYttFfUcSt37Wojwuea-gW530BRZ0QIz/view?usp=drive_link
# 5th step: extract the file id from the link: 1oYttFfUcSt37Wojwuea-gW530BRZ0QIz
# 6th step: replace the img src with https://lh3.googleusercontent.com/d/{gif-file-id}
# 7th step: 

st.markdown("<img src='https://lh3.googleusercontent.com/d/1oYttFfUcSt37Wojwuea-gW530BRZ0QIz' alt='windmill' style='display:block;margin-left:auto;margin-right:auto;'>", unsafe_allow_html=True)
