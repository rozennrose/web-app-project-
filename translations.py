# translations.py

TEXTS = {
    "Indonesia": {
        # Halaman Home
        "welcome": "👋 Selamat Datang! ✨",
        "home_desc": "Aplikasi ini memvisualisasikan konsep Matematika Diskrit.",
        "home_guide": "📖 Panduan: Pilih menu di samping untuk mulai.",
        
        # Halaman Profile (Label Umum)
        "profile_title": "Profil Tim",
        "contribution": "Kontribusi",
        "name_label": "Nama",
        "program_label": "Program Studi",
        
        # Point Kontribusi Profile
        "fina_points": [
            "Merancang dan mengimplementasikan antarmuka pengguna Streamlit dan navigasi multi-halaman.",
            "Mengembangkan konten dan gaya halaman 'Profil Tim'.",
            "Membuat halaman Visualisasi Graf (menampilkan graf, derajat simpul, dan matriks adjacency).",
            "Berpartisipasi dalam mendokumentasikan desain UI dan hasil dalam laporan akhir."
        ],
        "anne_points": [
            "Mengimplementasikan algoritma rute terpendek antar kota dan memproses data rute.",
            "Membuat halaman 'Graf Provinsi Lengkap' untuk Jawa Barat.",
            "Melakukan pengujian dan debugging algoritma graf serta akurasi dataset.",
            "Mendokumentasikan metode teknis (algoritma & sumber data).",
            "Mengumpulkan dan menyiapkan dataset koneksi kota untuk pulau Jawa."
        ],
        "alfa_points": [
            "Memimpin perencanaan proyek, lini masa, dan koordinasi.",
            "Mengoordinasikan integrasi algoritma rute terpendek ke dalam aplikasi.",
            "Mengelola repositori kode, deployment GitHub, dan deployment Streamlit Cloud."
        ],

        # Halaman Graph Visualization
        "graph_header": "Visualisasi Graf",
        "graph_desc": "Aplikasi ini mendemonstrasikan visualisasi graf sederhana dan properti dasarnya.",
        "nodes_input": "Masukkan Jumlah Titik (Nodes):",
        "edges_input": "Masukkan Jumlah Sisi (Edges):",
        "gen_btn": "Buat Graf",
        "prop_sub": "Properti Graf",
        "deg_title": "Derajat Setiap Titik",
        "adj_title": "Matriks Adjasensi",

        # Halaman Map Visualization
        "map_title": "Visualisasi Jaringan Pulau Jawa",
        "sel_prov": "Pilih Provinsi",
        "short_calc": "Kalkulator Jarak Terpendek",
        "start_city": "Kota Asal",
        "end_city": "Kota Tujuan",
        "calc_btn": "Hitung Rute Terpendek",
        "path_found": "Rute Terpendek Ditemukan!",
        "dist_total": "Total Jarak:",
        "path_list": "Rute:",
        "map_highlight": "Peta dengan Jalur Terpendek",
        "warning_no_data": "Tidak ada data untuk provinsi:",
        "no_path": "Tidak ada jalur yang ditemukan."
    },
    "English": {
        # Home Page
        "welcome": "👋 Welcome! ✨",
        "home_desc": "This app visualizes Discrete Mathematics concepts.",
        "home_guide": "📖 Guide: Select a menu on the side to start.",
        
        # Profile Page (Common Labels)
        "profile_title": "Team Profile",
        "contribution": "Contribution",
        "name_label": "Name",
        "program_label": "Program",
        
        # Profile Contribution Points
        "fina_points": [
            "Designed and implemented the Streamlit user interface and multi-page navigation.",
            "Developed the 'Team Profile' page content and styling.",
            "Created the Graph Visualization page (showing the graph, node degrees, and adjacency matrix).",
            "Participated in documenting UI design and results in the final report."
        ],
        "anne_points": [
            "Implemented the shortest-route algorithm between cities and processed route data.",
            "Created the 'Full Province Graph' page for West Java.",
            "Conducted testing and debugging of graph algorithms and dataset accuracy.",
            "Documented technical methods (algorithms & data sources).",
            "Collected and prepared dataset of city connections for Java."
        ],
        "alfa_points": [
            "Led project planning, timeline, and coordination.",
            "Coordinated integration of the shortest-route algorithm into the app.",
            "Managed code repository, GitHub deployment, and Streamlit Cloud deployment."
        ],

        # Graph Visualization Page
        "graph_header": "Graph Visualization",
        "graph_desc": "This application demonstrates simple graph visualization and its basic properties.",
        "nodes_input": "Enter Number of Nodes (Vertices):",
        "edges_input": "Enter Number of Edges (Sides):",
        "gen_btn": "Generate Graph",
        "prop_sub": "Graph Properties",
        "deg_title": "Degree of Each Node",
        "adj_title": "Adjacency Matrix",

        # Map Visualization Page
        "map_title": "Java Island Network Visualization",
        "sel_prov": "Select Province",
        "short_calc": "Shortest Distance Calculator",
        "start_city": "Start City",
        "end_city": "End City",
        "calc_btn": "Calculate Shortest Path",
        "path_found": "Shortest Path Found!",
        "dist_total": "Total Distance:",
        "path_list": "Path:",
        "map_highlight": "Map with Shortest Path Highlighted",
        "warning_no_data": "No cities available in:",
        "no_path": "No path found."
    }
}