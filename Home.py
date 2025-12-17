import streamlit as st
import sys
import os

# Menambahkan path agar folder utama terbaca oleh sub-halaman
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import dari file 'translations.py' (pastikan pakai 's' sesuai nama file baru Anda)
try:
    from translations import TEXTS
except ImportError:
    st.error("Error: File 'translations.py' tidak ditemukan. Pastikan nama file sudah benar.")

# Inisialisasi session state bahasa
if "lang" not in st.session_state:
    st.session_state["lang"] = "Indonesia"

# --- SIDEBAR UNTUK GANTI BAHASA ---
st.sidebar.title("Settings")
selected_lang = st.sidebar.selectbox(
    "Pilih Bahasa / Select Language", 
    ["Indonesia", "English"],
    index=0 if st.session_state["lang"] == "Indonesia" else 1
)

# Update pilihan bahasa
st.session_state["lang"] = selected_lang
t = TEXTS[st.session_state["lang"]]

# --- KONTEN HALAMAN UTAMA ---
st.title(t["welcome"]) # Pastikan key 'welcome' ada di translations.py

st.markdown("---")

# Deskripsi Proyek
if st.session_state["lang"] == "Indonesia":
    st.markdown("""
    ### Selamat Datang di Proyek Matematika Diskrit!
    Aplikasi ini menggunakan **Teori Graf** untuk memodelkan jaringan transportasi di Pulau Jawa. 
    Kami menggunakan **Algoritma Dijkstra** untuk menghitung rute terpendek antar kota.
    
    **Fitur Utama:**
    * **Visualisasi Graf:** Melihat matriks ketetangga (Adjacency Matrix).
    * **Peta Interaktif:** Mencari jalur tercepat di peta Pulau Jawa.
    * **Analisis Matematika:** Menghitung derajat simpul dan jarak total.
    """)
else:
    st.markdown("""
    ### Welcome to the Discrete Mathematics Project!
    This application utilizes **Graph Theory** to model the transportation network in Java. 
    We use **Dijkstra's Algorithm** to calculate the shortest routes between cities.
    
    **Key Features:**
    * **Graph Visualization:** View Adjacency Matrices and node properties.
    * **Interactive Map:** Find the fastest path on the Java Island map.
    * **Mathematical Analysis:** Calculate node degrees and total distances.
    """)