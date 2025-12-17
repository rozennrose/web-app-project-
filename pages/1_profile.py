import streamlit as st
import sys
import os

# Solusi agar sub-page bisa baca file di folder utama
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from translations import TEXTS

# Language selection logic (consistent with your other pages)
if "lang" not in st.session_state:
    st.session_state["lang"] = "Indonesia"

# Sidebar to switch language
selected_lang = st.sidebar.selectbox("Language / Bahasa", ["Indonesia", "English"], 
                                     index=0 if st.session_state["lang"] == "Indonesia" else 1)
st.session_state["lang"] = selected_lang
t = TEXTS[st.session_state["lang"]]

st.title(t["profile_title"])

# Data linked to translation keys
members = [
    {
        "name": "Fina Nailatul Fadhilah",
        "program": "Actuarial Science",
        "id": "021202500023",
        "image": "images/fina.jpg",
        "contribution": t["fina_points"]
    },
    {
        "name": "Roseanne Nugraheni",
        "program": "Actuarial Science",
        "id": "021202500022",
        "image": "images/anne.jpg",
        "contribution": t["anne_points"]
    },
    {
        "name": "Rega Alfarizi",
        "program": "Actuarial Science",
        "id": "021202500003",
        "image": "images/alfa.jpg",
        "contribution": t["alfa_points"]
    }
]

cols = st.columns(3)
for col, member in zip(cols, members):
    with col:
        st.image(member["image"], width=150)
        # Use dynamic labels for Name and Program
        st.markdown(f"**{t['name_label']}:** {member['name']}  \n**{t['program_label']}:** {member['program']}\n{member['id']}")
        with st.expander(f"📌 {t['contribution']}"):
            for point in member["contribution"]:
                st.markdown(f"- {point}")