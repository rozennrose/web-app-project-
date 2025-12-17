import streamlit as st
import subprocess
import sys
import os

st.set_page_config(page_title="Discrete Project", page_icon="🌐")

st.title("🌐 Pilih Bahasa / Choose Language")

language = st.radio(
    "Pilih bahasa yang ingin kamu gunakan:",
    ["Bahasa Indonesia", "English"]
)

if st.button("Lanjut / Continue"):
    if language == "Bahasa Indonesia":
        # jalankan versi lama
        os.system(f"{sys.executable} main.py")
    else:
        # jalankan versi bahasa Inggris
        os.system(f"{sys.executable} main_en.py")
