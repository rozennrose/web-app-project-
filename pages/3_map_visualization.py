import streamlit as st
import folium
from streamlit_folium import folium_static
import networkx as nx
import math 
import sys
import os

# --- TRANSLATION DICTIONARY ---
# If your translations.py is already set up, you can keep the import.
# I've included a local version here just in case.
TEXTS = {
    "English": {
        "title": "Java Island Network Visualization",
        "select_prov": "Select Province",
        "map_header": "Network Map",
        "calc_header": "Shortest Distance Calculator",
        "start_city": "Start City",
        "end_city": "End City",
        "btn_calc": "Calculate Shortest Path",
        "success": "Shortest Path Found!",
        "total_dist": "Total Distance",
        "path": "Path",
        "map_highlight": "Map with Shortest Path Highlighted",
        "no_path": "No path found connecting",
        "warning_select": "Please select both a Start City and an End City.",
        "warning_no_data": "No cities available to visualize in"
    },
    "Indonesia": {
        "title": "Visualisasi Jaringan Pulau Jawa",
        "select_prov": "Pilih Provinsi",
        "map_header": "Peta Jaringan",
        "calc_header": "Kalkulator Jarak Terpendek",
        "start_city": "Kota Asal",
        "end_city": "Kota Tujuan",
        "btn_calc": "Hitung Jalur Terpendek",
        "success": "Jalur Terpendek Ditemukan!",
        "total_dist": "Total Jarak",
        "path": "Rute",
        "map_highlight": "Peta dengan Sorotan Jalur Terpendek",
        "no_path": "Tidak ada jalur yang menghubungkan",
        "warning_select": "Silakan pilih Kota Asal dan Kota Tujuan.",
        "warning_no_data": "Tidak ada data kota untuk divisualisasikan di"
    }
}

# Language Selector
if "lang" not in st.session_state:
    st.session_state["lang"] = "Indonesia"

selected_lang = st.sidebar.selectbox("Language / Bahasa", ["Indonesia", "English"], index=0)
st.session_state["lang"] = selected_lang
t = TEXTS[st.session_state["lang"]]

# --- MATHEMATICAL LOGIC ---
def haversine_distance(coord1, coord2):
    """Calculate the great-circle distance in kilometers."""
    R = 6371 
    lat1, lon1 = coord1; lat2, lon2 = coord2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- DATA STRUCTURE (NODES and EDGES) ---
JAVA_NODES = {
    # West Java
    "Bandung": {"lat": -6.9174, "lon": 107.6191, "province": "West Java"}, "Bekasi": {"lat": -6.2384, "lon": 106.9751, "province": "West Java"},
    "Bogor": {"lat": -6.5950, "lon": 106.8166, "province": "West Java"}, "Cirebon": {"lat": -6.7350, "lon": 108.5584, "province": "West Java"},
    "Sukabumi": {"lat": -6.9213, "lon": 106.9248, "province": "West Java"}, "Purwakarta": {"lat": -6.5599, "lon": 107.4475, "province": "West Java"},
    "Karawang": {"lat": -6.3075, "lon": 107.3072, "province": "West Java"}, "Tasikmalaya": {"lat": -7.3275, "lon": 108.2175, "province": "West Java"},
    "Ciamis": {"lat": -7.3300, "lon": 108.3500, "province": "West Java"}, "Cianjur": {"lat": -6.8200, "lon": 107.1300, "province": "West Java"},
    "Garut": {"lat": -7.2172, "lon": 107.8931, "province": "West Java"}, "Indramayu": {"lat": -6.3263, "lon": 108.3292, "province": "West Java"},
    "Kuningan": {"lat": -6.9806, "lon": 108.4878, "province": "West Java"}, "Majalengka": {"lat": -6.8375, "lon": 108.2272, "province": "West Java"},
    "Pangandaran": {"lat": -7.6744, "lon": 108.3072, "province": "West Java"}, "Subang": {"lat": -6.5647, "lon": 107.7538, "province": "West Java"},
    "Sumedang": {"lat": -6.8500, "lon": 107.9167, "province": "West Java"}, "Cimahi": {"lat": -6.8739, "lon": 107.5452, "province": "West Java"},
    "Depok": {"lat": -6.4025, "lon": 106.7958, "province": "West Java"},
    # Central Java
    "Banjarnegara": {"lat": -7.3972, "lon": 109.6917, "province": "Central Java"}, "Banyumas": {"lat": -7.4206, "lon": 109.2312, "province": "Central Java"},
    "Batang": {"lat": -6.9200, "lon": 109.7300, "province": "Central Java"}, "Blora": {"lat": -6.9800, "lon": 111.3900, "province": "Central Java"},
    "Boyolali": {"lat": -7.5300, "lon": 110.6000, "province": "Central Java"}, "Brebes": {"lat": -6.8778, "lon": 109.0436, "province": "Central Java"},
    "Cilacap": {"lat": -7.7119, "lon": 109.0069, "province": "Central Java"}, "Demak": {"lat": -6.8833, "lon": 110.6333, "province": "Central Java"},
    "Grobogan": {"lat": -7.0300, "lon": 110.8700, "province": "Central Java"}, "Jepara": {"lat": -6.5833, "lon": 110.6500, "province": "Central Java"},
    "Karanganyar": {"lat": -7.5800, "lon": 111.0500, "province": "Central Java"}, "Kebumen": {"lat": -7.6667, "lon": 109.6667, "province": "Central Java"},
    "Kendal": {"lat": -6.9700, "lon": 110.2000, "province": "Central Java"}, "Klaten": {"lat": -7.7200, "lon": 110.6000, "province": "Central Java"},
    "Kudus": {"lat": -6.8000, "lon": 110.8333, "province": "Central Java"}, "Magelang": {"lat": -7.4739, "lon": 110.2198, "province": "Central Java"},
    "Pati": {"lat": -6.7800, "lon": 111.0300, "province": "Central Java"}, "Pekalongan": {"lat": -6.8858, "lon": 109.6797, "province": "Central Java"},
    "Pemalang": {"lat": -6.8900, "lon": 109.4000, "province": "Central Java"}, "Purbalingga": {"lat": -7.2667, "lon": 109.3667, "province": "Central Java"},
    "Purworejo": {"lat": -7.7200, "lon": 110.0000, "province": "Central Java"}, "Rembang": {"lat": -6.7000, "lon": 111.3333, "province": "Central Java"},
    "Semarang": {"lat": -6.9667, "lon": 110.4167, "province": "Central Java"}, "Sragen": {"lat": -7.4167, "lon": 110.9833, "province": "Central Java"},
    "Sukoharjo": {"lat": -7.6700, "lon": 110.8300, "province": "Central Java"}, "Tegal": {"lat": -6.8778, "lon": 109.1126, "province": "Central Java"},
    "Temanggung": {"lat": -7.3167, "lon": 110.1667, "province": "Central Java"}, "Wonogiri": {"lat": -7.8300, "lon": 110.9500, "province": "Central Java"},
    "Wonosobo": {"lat": -7.3600, "lon": 109.9000, "province": "Central Java"}, "Salatiga": {"lat": -7.3300, "lon": 110.5000, "province": "Central Java"},
    "Surakarta": {"lat": -7.5667, "lon": 110.8333, "province": "Central Java"}, "KotaTegal": {"lat": -6.8778, "lon": 109.1126, "province": "Central Java"}, 
    "Yogyakarta": {"lat": -7.7956, "lon": 110.3695, "province": "Central Java"},
    # East Java
    "Bangkalan": {"lat": -7.0500, "lon": 112.7500, "province": "East Java"}, "Banyuwangi": {"lat": -8.2167, "lon": 114.3667, "province": "East Java"},
    "BlitarKab": {"lat": -8.0945, "lon": 112.3364, "province": "East Java"}, "Bojonegoro": {"lat": -7.2272, "lon": 111.8847, "province": "East Java"},
    "Bondowoso": {"lat": -7.9167, "lon": 113.8333, "province": "East Java"}, "Gresik": {"lat": -7.1685, "lon": 112.6517, "province": "East Java"},
    "Jember": {"lat": -8.1738, "lon": 113.7001, "province": "East Java"}, "Jombang": {"lat": -7.5300, "lon": 112.2300, "province": "East Java"},
    "KediriKab": {"lat": -7.8289, "lon": 112.0085, "province": "East Java"}, "Lamongan": {"lat": -7.1278, "lon": 112.4178, "province": "East Java"},
    "Lumajang": {"lat": -8.1667, "lon": 112.9333, "province": "East Java"}, "MadiunKab": {"lat": -7.6291, "lon": 111.5284, "province": "East Java"},
    "Magetan": {"lat": -7.6500, "lon": 111.3500, "province": "East Java"}, "MalangKab": {"lat": -7.9839, "lon": 112.6321, "province": "East Java"},
    "Mojokerto": {"lat": -7.4561, "lon": 112.4333, "province": "East Java"}, "Nganjuk": {"lat": -7.5900, "lon": 111.8600, "province": "East Java"},
    "Ngawi": {"lat": -7.4000, "lon": 111.1667, "province": "East Java"}, "Pacitan": {"lat": -8.1800, "lon": 111.1000, "province": "East Java"},
    "Pamekasan": {"lat": -7.1667, "lon": 113.4667, "province": "East Java"}, "Pasuruan": {"lat": -7.6536, "lon": 112.9097, "province": "East Java"},
    "Ponorogo": {"lat": -7.8667, "lon": 111.4833, "province": "East Java"}, "Probolinggo": {"lat": -7.7500, "lon": 113.2167, "province": "East Java"},
    "Sampang": {"lat": -7.2000, "lon": 113.3000, "province": "East Java"}, "Sidoarjo": {"lat": -7.4526, "lon": 112.7167, "province": "East Java"},
    "Situbondo": {"lat": -7.7167, "lon": 114.0000, "province": "East Java"}, "Sumenep": {"lat": -7.0000, "lon": 113.8833, "province": "East Java"},
    "Trenggalek": {"lat": -8.0833, "lon": 111.7000, "province": "East Java"}, "Tuban": {"lat": -6.8900, "lon": 112.0600, "province": "East Java"},
    "Tulungagung": {"lat": -8.0667, "lon": 111.9000, "province": "East Java"}, "BlitarKota": {"lat": -8.1000, "lon": 112.1667, "province": "East Java"},
    "Batu": {"lat": -7.8700, "lon": 112.5200, "province": "East Java"}, "KediriKota": {"lat": -7.8289, "lon": 112.0085, "province": "East Java"},
    "MadiunKota": {"lat": -7.6291, "lon": 111.5284, "province": "East Java"}, "Surabaya": {"lat": -7.2575, "lon": 112.7521, "province": "East Java"},
}

JAVA_EDGES = [
    ("Bogor", "Depok"), ("Bogor", "Cianjur"), ("Depok", "Bekasi"), ("Bekasi", "Karawang"), ("Karawang", "Purwakarta"),
    ("Purwakarta", "Subang"), ("Bandung", "Cimahi"), ("Bandung", "Sumedang"), ("Bandung", "Garut"), ("Garut", "Tasikmalaya"),
    ("Tasikmalaya", "Ciamis"), ("Ciamis", "Pangandaran"), ("Sumedang", "Majalengka"), ("Majalengka", "Cirebon"),
    ("Cirebon", "Kuningan"), ("Cirebon", "Indramayu"), ("Indramayu", "Subang"), ("Bogor", "Sukabumi"), ("Cianjur", "Bandung"),
    ("Cirebon", "Brebes"), ("Kuningan", "Brebes"), ("Ciamis", "Cilacap"), ("Pangandaran", "Cilacap"),
    ("Brebes", "Tegal"), ("Tegal", "Pemalang"), ("Pemalang", "Pekalongan"), ("Pekalongan", "Batang"), ("Batang", "Kendal"),
    ("Kendal", "Semarang"), ("Semarang", "Demak"), ("Semarang", "Salatiga"), ("Demak", "Kudus"), ("Kudus", "Jepara"),
    ("Kudus", "Pati"), ("Pati", "Rembang"), ("Rembang", "Blora"), ("Semarang", "Boyolali"), ("Boyolali", "Surakarta"),
    ("Surakarta", "Karanganyar"), ("Surakarta", "Sukoharjo"), ("Sukoharjo", "Wonogiri"), ("Wonogiri", "Sragen"),
    ("Surakarta", "Klaten"), ("Klaten", "Yogyakarta"), ("Yogyakarta", "Magelang"), ("Magelang", "Temanggung"),
    ("Temanggung", "Wonosobo"), ("Wonosobo", "Banjarnegara"), ("Banjarnegara", "Purbalingga"), ("Purbalingga", "Banyumas"),
    ("Banyumas", "Cilacap"), ("Banyumas", "Kebumen"), ("Kebumen", "Purworejo"), ("Purworejo", "Yogyakarta"),
    ("Surakarta", "Ngawi"), ("Pacitan", "Wonogiri"), ("Blora", "Tuban"), ("Rembang", "Tuban"), 
    ("Ngawi", "Magetan"), ("Magetan", "MadiunKab"), ("MadiunKab", "MadiunKota"), ("MadiunKota", "Ponorogo"), ("Ponorogo", "Trenggalek"),
    ("Trenggalek", "Tulungagung"), ("Tulungagung", "KediriKab"), ("KediriKab", "KediriKota"), ("KediriKota", "Nganjuk"),
    ("Nganjuk", "Jombang"), ("Jombang", "Mojokerto"), ("Mojokerto", "Sidoarjo"), ("Sidoarjo", "Surabaya"),
    ("Surabaya", "Gresik"), ("Gresik", "Lamongan"), ("Lamongan", "Tuban"), ("Mojokerto", "MalangKab"),
    ("MalangKab", "Batu"), ("MalangKab", "Lumajang"), ("Lumajang", "Jember"), ("Jember", "Bondowoso"),
    ("Bondowoso", "Situbondo"), ("Situbondo", "Banyuwangi"), ("MalangKab", "Pasuruan"), ("Pasuruan", "Probolinggo"),
    ("Sidoarjo", "Pasuruan"), ("Pasuruan", "BlitarKab"), ("BlitarKab", "BlitarKota"), ("BlitarKota", "KediriKab"),
    ("Surabaya", "Bangkalan"), ("Bangkalan", "Sampang"), ("Sampang", "Pamekasan"), ("Pamekasan", "Sumenep"),
]

# --- UTILITY FUNCTIONS ---
def get_province_nodes(selected_province):
    if selected_province == "Java (All)": return JAVA_NODES
    return {city: data for city, data in JAVA_NODES.items() if data["province"] == selected_province}

def get_province_edges(selected_province):
    if selected_province == "Java (All)": return JAVA_EDGES
    nodes_in_province = list(get_province_nodes(selected_province).keys())
    return [(u, v) for u, v in JAVA_EDGES if u in nodes_in_province and v in nodes_in_province]

def create_network_graph(selected_province):
    G = nx.Graph()
    nodes_data = get_province_nodes(selected_province)
    edges_list = get_province_edges(selected_province)
    for city, data in nodes_data.items(): G.add_node(city, **data) 
    for u, v in edges_list:
        if G.has_node(u) and G.has_node(v):
            coord_u = (G.nodes[u]['lat'], G.nodes[u]['lon'])
            coord_v = (G.nodes[v]['lat'], G.nodes[v]['lon'])
            G.add_edge(u, v, weight=haversine_distance(coord_u, coord_v))
    return G

def render_map(G, path=None, center=(-7.0, 110.0), zoom_start=7):
    m = folium.Map(location=center, zoom_start=zoom_start, tiles="cartodbpositron")
    for u, v, d in G.edges(data=True):
        coords = [(G.nodes[u]["lat"], G.nodes[u]["lon"]), (G.nodes[v]["lat"], G.nodes[v]["lon"])]
        tooltip_text = f"{u} - {v}"
        if path is None: tooltip_text += f" ({d['weight']:.2f} km)"
        folium.PolyLine(coords, weight=1.5, opacity=0.6, color='gray', tooltip=tooltip_text).add_to(m)
    for n, d in G.nodes(data=True):
        folium.CircleMarker(location=[d["lat"], d["lon"]], radius=4, color='blue', fill=True, popup=f"<b>{n}</b><br>{d['province']}").add_to(m)
    if path:
        path_coords = [(G.nodes[city]["lat"], G.nodes[city]["lon"]) for city in path]
        folium.PolyLine(path_coords, weight=4, color="red", opacity=1.0).add_to(m)
        folium.CircleMarker(location=path_coords[0], radius=8, color='green', fill=True, popup=f"START: {path[0]}").add_to(m)
        folium.CircleMarker(location=path_coords[-1], radius=8, color='darkred', fill=True, popup=f"END: {path[-1]}").add_to(m)
    return m

# --- MAIN APP ---
def main():
    st.title(t["title"])
    PROVINCE_OPTIONS = ["Java (All)", "West Java", "Central Java", "East Java"]
    selected_province = st.selectbox(t["select_prov"], PROVINCE_OPTIONS)
    
    if selected_province == "West Java": map_center, map_zoom = (-6.9, 107.5), 8
    elif selected_province == "Central Java": map_center, map_zoom = (-7.5, 110.5), 8
    elif selected_province == "East Java": map_center, map_zoom = (-7.8, 112.5), 7.5
    else: map_center, map_zoom = (-7.0, 110.0), 7
    
    G = create_network_graph(selected_province)
    available_cities = sorted(list(G.nodes))
    
    if available_cities:
        st.header(f"{t['map_header']}: {selected_province}")
        m = render_map(G, center=map_center, zoom_start=map_zoom)
        folium_static(m)
        
        st.markdown("---")
        st.header(t["calc_header"])
        
        col1, col2 = st.columns(2)
        with col1: start_city = st.selectbox(t["start_city"], available_cities, index=available_cities.index("Bandung") if "Bandung" in available_cities else 0)
        with col2: end_city = st.selectbox(t["end_city"], [c for c in available_cities if c != start_city], index=available_cities.index("Surabaya") if "Surabaya" in available_cities else 0)
            
        if st.button(t["btn_calc"]):
            try:
                shortest_path = nx.shortest_path(G, source=start_city, target=end_city, weight='weight')
                shortest_distance = nx.shortest_path_length(G, source=start_city, target=end_city, weight='weight')
                st.success(f"✅ **{t['success']}**")
                st.info(f"**{t['total_dist']}:** {shortest_distance:.2f} KM")
                st.write(f"**{t['path']}:** {' → '.join(shortest_path)}")
                
                st.subheader(t["map_highlight"])
                m_path = render_map(G, path=shortest_path, center=map_center, zoom_start=map_zoom)
                folium_static(m_path)
            except nx.NetworkXNoPath:
                st.error(f"❌ {t['no_path']} {start_city} & {end_city}.")
    else:
        st.warning(f"{t['warning_no_data']} {selected_province}.")

if __name__ == "__main__":
    main()