import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image

import base64
import time

# =========================
# LOAD MODEL
# =========================
model = load_model("NASNetMobile.h5")

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Sistem Deteksi Daun Singkong",
    layout="centered"
)

# =========================
# CSS CUSTOM
# =========================
st.markdown("""
<style>

/* BUTTON */
.stButton > button {
    width: 100%;
    border-radius: 15px;
    height: 60px;
    font-size: 18px;
}

/* CARD MENU */
.menu-card{
    background-color:white;
    padding:25px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 2px 10px rgba(0,0,0,0.1);
    transition:0.3s;
}

.menu-card:hover{
    transform:scale(1.03);
}

/* CARD JENIS DAUN */
.card {
    display: flex;
    align-items: center;
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.card img {
    width: 80px;
    height: 80px;
    object-fit: contain;
    margin-right: 15px;
}

.card-title {
    font-size: 18px;
    font-weight: bold;
}

.card-desc {
    font-size: 14px;
    color: #555;
}

/* LABEL FILE UPLOADER */
[data-testid="stFileUploader"] label {
    width: 100%;
    text-align: center;
    display: block;
    font-size: 18px;
    font-weight: bold;
}

/* INFO BOX */
.info-box{
    background-color:#f8f9fa;
    padding:20px;
    border-radius:15px;
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
}

/* TITLE */
.title-text{
    font-size:22px;
    font-weight:bold;
    color:#2E2E3A;
}

/* DESC */
.desc-text{
    font-size:16px;
    text-align:justify;
    color:#555;
}

</style>
""", unsafe_allow_html=True)

# =========================
# FUNCTION BASE64
# =========================
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# =========================
# SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "splash"

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# =========================
# SPLASH SCREEN
# =========================
def splash_screen():

    st.markdown("""
        <h1 style='text-align:center;font-size:55px;font-weight:bold;color:#2E2E3A;'>
            Sistem Deteksi Daun Singkong
        </h1>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    daun_base64 = get_base64("daun.png")

    st.markdown(f"""
        <div style='text-align:center;'>
            <img src="data:image/png;base64,{daun_base64}" width="170">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    progress = st.progress(0)

    progress.progress(100)
    time.sleep(1)

    st.session_state.page = "menu"
    st.rerun()

# =========================
# MENU UTAMA
# =========================
def menu_utama():

    st.markdown("""
    <h1 style='text-align:center;font-size:50px;font-weight:bold;color:#2E2E3A;'>
        Selamat datang di <br>
        Sistem Deteksi Daun Singkong
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    kamera_base64 = get_base64("kamera.jpg")
    jenis_base64 = get_base64("jenis.jpg")
    info_base64 = get_base64("informasi.jpg")
    hasil_base64 = get_base64("hasil deteksi.jpg")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # DETEKSI
    with col1:
        st.markdown(f"""
            <div class="menu-card">
                <img src="data:image/png;base64,{kamera_base64}" width="170">
            </div>
        """, unsafe_allow_html=True)

        if st.button("Upload Gambar", key="menu_kamera"):
            st.session_state.page = "kamera"
            st.rerun()

    # JENIS DAUN
    with col2:
        st.markdown(f"""
            <div class="menu-card">
                <img src="data:image/png;base64,{jenis_base64}" width="170">
            </div>
        """, unsafe_allow_html=True)

        if st.button("Jenis Daun", key="menu_jenis"):
            st.session_state.page = "jenis"
            st.rerun()

    # INFORMASI
    with col3:
        st.markdown(f"""
            <div class="menu-card">
                <img src="data:image/png;base64,{info_base64}" width="170">
            </div>
        """, unsafe_allow_html=True)

        if st.button("Informasi", key="menu_info"):
            st.session_state.page = "informasi"
            st.rerun()

    # RIWAYAT
    with col4:
        st.markdown(f"""
            <div class="menu-card">
                <img src="data:image/png;base64,{hasil_base64}" width="170">
            </div>
        """, unsafe_allow_html=True)

        if st.button("Riwayat Deteksi", key="menu_riwayat"):
            st.session_state.page = "riwayat"
            st.rerun()

# =========================
# HALAMAN KAMERA
# =========================
def halaman_kamera():

    st.markdown("""
    <h1 style='text-align:center;'>
        Deteksi Daun Singkong
    </h1>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
    "Upload file"
    )

    if uploaded_file:
        ekstensi_valid = ["jpg", "jpeg", "png"]

        ekstensi_file = uploaded_file.name.split(".")[-1].lower()

        if ekstensi_file not in ekstensi_valid:
            st.error("File tidak valid. Silakan upload file gambar JPG, JPEG, atau PNG.")
            return
        
        try:
            img = Image.open(uploaded_file)
            img.verify()
        except:
            st.error("File yang diunggah bukan gambar yang valid.")
            return

        st.image(uploaded_file, width=300)

        if st.button("🔍 Proses Deteksi", key="btn_deteksi"):

            # PREPROCESS IMAGE
            img = Image.open(uploaded_file).convert("RGB")
            img = img.resize((224, 224))

            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # PREDICT
            pred = model.predict(img_array)

            kelas = np.argmax(pred)
            confidence = np.max(pred) * 100

            # LABEL
            labels = ["Karet", "Papua", "Sayur"]

            #THRESHOLD
            THRESHOLD = 80
            if confidence < THRESHOLD:

                st.session_state.hasil = "Tidak Dikenali"
                st.session_state.confidence = confidence
                st.session_state.image = uploaded_file

                st.session_state.riwayat.append({
                    "hasil": "Tidak Dikenali",
                    "confidence": confidence,
                    "image": uploaded_file.getvalue()
                })

                st.session_state.page = "hasil_deteksi"
                st.rerun()

            else:

                st.session_state.hasil = labels[kelas]
                st.session_state.confidence = confidence
                st.session_state.image = uploaded_file

                #simpan ke riwayat
                st.session_state.riwayat.append({
                    "hasil": labels[kelas],
                     "confidence": confidence,
                    "image": uploaded_file.getvalue()
                })

                #pindah ke halaman hasil deteksi
                st.session_state.page = "hasil_deteksi"
                st.rerun()

    if st.button("⬅️ Kembali", key="btn_kamera"):
        st.session_state.page = "menu"
        st.rerun()

# =========================
# HALAMAN HASIL
# =========================
def hasil_deteksi():
    st.markdown("<h1 style='text-align:center;'>Hasil Deteksi</h1>", unsafe_allow_html=True)

    # =========================
    # DATA LENGKAP
    # =========================
    data = {
        "Karet": {
            "nama": "Daun Singkong Karet",
            "jenis": "Memiliki daun besar, lebar, dan rimbun dengan warna hijau tua serta pertumbuhan tanaman yang cepat dan batang kuat.",
            "info": "Menghasilkan umbi beracun dengan kandungan sianida tinggi sehingga tidak untuk konsumsi. Daun harus dimasak atau dijemur terlebih dahulu sebelum digunakan, baik sebagai sayuran maupun pakan ternak."
        },

        "Papua": {
            "nama": "Daun Singkong Papua",
            "jenis": "Memiliki daun lebar menjari dengan 3-5 lobus besar. Batang kokoh, berkayu lunak.",
            "info": "Daun mengandung kadar sianida alami yang cukup tinggi, sehingga perlu dijemur atau dilayukan terlebih dahulu sebelum diberikan kepada ternak. Tanaman ini lebih difokuskan pada produksi daun dan tidak menghasilkan umbi yang dapat dikonsumsi."
        },

        "Sayur": {
            "nama": "Daun Singkong Sayur",
            "jenis": "Memiliki batang kecil dengan daun sempit, rimbun, serta bentuk daun menjari yang ramping, panjang, dan runcing dengan tangkai daun yang panjang.",
            "info": "Daun singkong ini bertekstur lembut, tidak kaku, dan tidak langu. Daun muda dipanen untuk sayur dan dapat dipanen kembali sekitar 15 hari setelah dipetik. Singkong ini khusus dibudidayakan untuk produksi daun sehingga tidak menghasilkan umbi konsumsi. Daun harus dimasak sebelum dikonsumsi."
        },

        "Tidak Dikenali": {
            "nama": "Gambar Tidak Dikenali",
            "jenis": "Gambar yang diunggah bukan merupakan daun singkong yang menjadi ruang lingkup aplikasi.",
            "info": "Sistem hanya mengenali: Daun Singkong Karet, Daun Singkong Papua, Daun Singkong Sayur"
        }
    }

    # =========================
    # CEK HASIL DETEKSI
    # =========================
    if "hasil" in st.session_state and st.session_state.hasil in data:

        hasil = st.session_state.hasil
        detail = data[hasil]

        # Layout tengah
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if "image" in st.session_state:
                colA, colB, colC = st.columns([1.5, 1, 1.5])
                with colB:
                    st.image(st.session_state.image, width=250)

            # Judul & confidence
            st.markdown(f"""
                <div style='text-align:center;'>
                    <h3>{detail['nama']}</h3>
                    <p><b>Confidence:</b> {st.session_state.get('confidence', 0):.2f}%</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # Jenis daun
            st.markdown("<h4 style='text-align:center;'>Jenis Daun</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;'>{detail['jenis']}</p>", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # Informasi daun
            st.markdown("<h4 style='text-align:center;'>Informasi Daun</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;'>{detail['info']}</p>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Tombol kembali
            if st.button("⬅️ Kembali", use_container_width=True, key="btn_hasil"):
                st.session_state.page = "kamera"
                st.rerun()

    else:
        st.warning("Belum ada hasil deteksi.")

        if st.button("⬅️ Kembali", use_container_width=True, key="btn_kosong"):
            st.session_state.page = "menu"
            st.rerun()

# =========================
# HALAMAN INFORMASI
# =========================
def halaman_informasi():

    st.markdown("<h1 style='text-align:center;'>Informasi Daun Singkong</h1>", unsafe_allow_html=True)

    data = [
        {
            "title": "Daun Singkong Karet",
            "desc": "Menghasilkan umbi beracun dengan kandungan sianida tinggi sehingga tidak untuk konsumsi. Daun harus dimasak atau dijemur terlebih dahulu sebelum digunakan, baik sebagai sayuran maupun pakan ternak.",
            "img": "daun singkong karet.PNG"
        },
        {
            "title": "Daun Singkong Papua",
            "desc": "Daun mengandung kadar sianida alami yang cukup tinggi, sehingga perlu dijemur atau dilayukan terlebih dahulu sebelum diberikan kepada ternak. Tanaman ini lebih difokuskan pada produksi daun dan tidak menghasilkan umbi yang dapat dikonsumsi.",
            "img": "daun singkong papua.PNG"
        },
        {
            "title": "Daun Singkong Sayur",
            "desc": "Daun singkong ini bertekstur lembut, tidak kaku, dan tidak langu. Daun muda dipanen untuk sayur dan dapat dipanen kembali sekitar 15 hari setelah dipetik. Singkong ini khusus dibudidayakan untuk produksi daun sehingga tidak menghasilkan umbi konsumsi. Daun harus dimasak sebelum dikonsumsi.",
            "img": "daun singkong sayur.PNG"
        }
    ]

    for item in data:
        img_base64 = get_base64(item["img"])

        st.markdown(f"""
        <div class="card">
            <img src="data:image/png;base64,{img_base64}">
            <div>
                <div class="card-title">{item['title']}</div>
                <div class="card-desc">{item['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("⬅️ Kembali", key="btn_informasi"):
        st.session_state.page = "menu"
        st.rerun()

# =========================
# HALAMAN RIWAYAT
# =========================
def halaman_riwayat():

    st.markdown(
        "<h1 style='text-align:center;'>Riwayat Deteksi</h1>",
        unsafe_allow_html=True
    )

    if len(st.session_state.riwayat) == 0:
        st.info("Belum ada riwayat deteksi.")

    else:

        data = {
            "Karet": {
                "nama": "Daun Singkong Karet",
                "jenis": "Memiliki daun besar, lebar, dan rimbun dengan warna hijau tua serta pertumbuhan tanaman yang cepat dan batang kuat.",
                "info": "Menghasilkan umbi beracun dengan kandungan sianida tinggi sehingga tidak untuk konsumsi. Daun harus dimasak atau dijemur terlebih dahulu sebelum digunakan, baik sebagai sayuran maupun pakan ternak."
            },

            "Papua": {
                "nama": "Daun Singkong Papua",
                "jenis": "Memiliki daun lebar menjari dengan 3-5 lobus besar. Batang kokoh, berkayu lunak.",
                "info": "Daun mengandung kadar sianida alami yang cukup tinggi, sehingga perlu dijemur atau dilayukan terlebih dahulu sebelum diberikan kepada ternak. Tanaman ini lebih difokuskan pada produksi daun dan tidak menghasilkan umbi yang dapat dikonsumsi."
            },

            "Sayur": {
                "nama": "Daun Singkong Sayur",
                "jenis": "Memiliki batang kecil dengan daun sempit, rimbun, serta bentuk daun menjari yang ramping, panjang, dan runcing dengan tangkai daun yang panjang.",
                "info": "Daun singkong ini bertekstur lembut, tidak kaku, dan tidak langu. Daun muda dipanen untuk sayur dan dapat dipanen kembali sekitar 15 hari setelah dipetik. Singkong ini khusus dibudidayakan untuk produksi daun sehingga tidak menghasilkan umbi konsumsi. Daun harus dimasak sebelum dikonsumsi."
            },
            "Tidak Dikenali": {
                "nama": "Gambar Tidak Dikenali",
                "jenis": "Gambar yang diunggah bukan merupakan daun singkong yang menjadi ruang lingkup aplikasi.",
                "info": "Sistem hanya mengenali: Daun Singkong Karet, Daun Singkong Papua, Daun Singkong Sayur"
            }
        }

        # tampilkan riwayat terbaru
        item = st.session_state.riwayat[-1]

        detail = data[item["hasil"]]

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            st.image(item["image"], width=250)

            st.markdown(f"""
            <div style='text-align:center;'>
                <h3>{detail['nama']}</h3>
                <p><b>Confidence:</b> {item['confidence']:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown(
                "<h4 style='text-align:center;'>Jenis Daun</h4>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<p style='text-align:center;'>{detail['jenis']}</p>",
                unsafe_allow_html=True
            )

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown(
                "<h4 style='text-align:center;'>Informasi Daun</h4>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<p style='text-align:center;'>{detail['info']}</p>",
                unsafe_allow_html=True
            )

    if st.button("⬅️ Kembali"):
        st.session_state.page = "menu"
        st.rerun()

# =========================
# HALAMAN JENIS
# =========================
def halaman_jenis():

    st.markdown("<h1 style='text-align:center;'>Jenis Daun Singkong</h1>", unsafe_allow_html=True)

    data = [
        {
            "title": "Daun Singkong Karet",
            "desc": "Memiliki daun besar, lebar, dan rimbun dengan warna hijau tua serta pertumbuhan tanaman yang cepat dan batang kuat.",
            "img": "daun singkong karet.PNG"
        },
        {
            "title": "Daun Singkong Papua",
            "desc": "Memiliki daun lebar menjari dengan 3-5 lobus besar. Batang kokoh, berkayu lunak.",
            "img": "daun singkong papua.PNG"
        },
        {
            "title": "Daun Singkong Sayur",
            "desc": "Memiliki batang kecil dengan daun sempit, rimbun, serta bentuk daun menjari yang ramping, panjang, dan runcing dengan tangkai daun yang panjang.",
            "img": "daun singkong sayur.PNG"
        }
    ]

    for item in data:
        img_base64 = get_base64(item["img"])

        st.markdown(f"""
        <div class="card">
            <img src="data:image/png;base64,{img_base64}">
            <div>
                <div class="card-title">{item['title']}</div>
                <div class="card-desc">{item['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("⬅️ Kembali", key="btn_jenis"):
        st.session_state.page = "menu"
        st.rerun()

# =========================
# ROUTING
# =========================
if st.session_state.page == "splash":
    splash_screen()

elif st.session_state.page == "menu":
    menu_utama()

elif st.session_state.page == "kamera":
    halaman_kamera()

elif st.session_state.page == "hasil_deteksi":
    hasil_deteksi()

elif st.session_state.page == "riwayat":
    halaman_riwayat()

elif st.session_state.page == "informasi":
    halaman_informasi()

elif st.session_state.page == "jenis":
    halaman_jenis()