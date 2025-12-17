import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd 
import sys
import os

# --- TRANSLATION DICTIONARY ---
# You can keep your import from translations.py, but here is the local structure:
TEXTS = {
    "English": {
        "graph_header": "Graph Theory Visualization",
        "graph_desc": "Explore fundamental graph properties: Degrees and Adjacency Matrices.",
        "nodes_input": "Number of Nodes",
        "edges_input": "Number of Edges",
        "gen_btn": "Generate Random Graph",
        "prop_sub": "Mathematical Properties",
        "deg_title": "Degree of Each Node",
        "adj_title": "Adjacency Matrix",
    },
    "Indonesia": {
        "graph_header": "Visualisasi Teori Graf",
        "graph_desc": "Eksplorasi properti fundamental graf: Derajat dan Matriks Adjacency.",
        "nodes_input": "Jumlah Simpul (Node)",
        "edges_input": "Jumlah Sisi (Edge)",
        "gen_btn": "Generate Graf Acak",
        "prop_sub": "Properti Matematis",
        "deg_title": "Derajat Setiap Simpul",
        "adj_title": "Matriks Adjacency",
    }
}

# Language Logic
if "lang" not in st.session_state:
    st.session_state["lang"] = "Indonesia"

# Sidebar selector for consistency across pages
selected_lang = st.sidebar.selectbox("Language / Bahasa", ["Indonesia", "English"], 
                                     index=0 if st.session_state["lang"] == "Indonesia" else 1)
st.session_state["lang"] = selected_lang
t = TEXTS[st.session_state["lang"]]

st.set_page_config(layout="wide")

def display_graph_properties(G):
    st.subheader(t["prop_sub"])
    
    st.markdown(f"#### {t['deg_title']}")
    degrees = dict(G.degree())
    degree_df = pd.DataFrame(degrees.items(), columns=['Node', 'Degree'])
    st.dataframe(degree_df, use_container_width=True)

    st.markdown(f"#### {t['adj_title']}")
    # Calculate the adjacency matrix
    adj_matrix_np = nx.adjacency_matrix(G).toarray()
    adj_matrix = pd.DataFrame(adj_matrix_np, index=list(G.nodes()), columns=list(G.nodes()))
    st.dataframe(adj_matrix, use_container_width=True)

def draw_graph(G):
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(G, pos, node_size=3000, node_color="#ADD8E6", 
                     edgecolors="black", linewidths=1.5, width=2, alpha=0.6, 
                     edge_color="gray", with_labels=True, font_size=12, 
                     font_weight="bold", ax=ax)
    st.pyplot(fig) 

# UI Elements using translated variables
st.header(t["graph_header"])
st.markdown(t["graph_desc"])
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    num_nodes = st.number_input(t["nodes_input"], min_value=2, max_value=15, value=5)
with col2:
    max_edges = int(num_nodes * (num_nodes - 1) / 2)
    num_edges = st.number_input(t["edges_input"], min_value=0, max_value=max_edges, value=min(6, max_edges))

if st.button(t["gen_btn"]):
    G = nx.gnm_random_graph(num_nodes, num_edges, seed=42)
    draw_graph(G)
    display_graph_properties(G)