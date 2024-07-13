import streamlit as st
import cv2
import tempfile
from PIL import Image
import os

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Arial', sans-serif;
    }
    .main-title {
        color: #007bff;
        text-align: center;
    }
    .sub-header {
        color: #6c757d;
    }
    .upload-box {
        border: 2px dashed #007bff;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        background-color: #e9ecef;
    }
    .button-style {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .button-style:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>📹 Aplikasi Pemrosesan Video ke Gambar</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-header'>✨ Unggah Video dan Ekstrak Frame ✨</h3>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Pilih file video", type=["mp4", "avi", "mov"], key='upload-box')

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    cap = cv2.VideoCapture(tfile.name)

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    st.write(f"Frame Rate: {frame_rate} FPS")
    st.write(f"Total Frames: {total_frames}")

    frame_number = st.slider("Pilih nomor frame", 0, total_frames - 1)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()

    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        st.image(image, caption=f'Frame {frame_number}', use_column_width=True)

        # Meminta pengguna untuk menentukan direktori penyimpanan dan nama file
        save_path = st.text_input("Masukkan path direktori untuk menyimpan gambar (misalnya, C:/Users/username/Documents/):")
        file_name = st.text_input("Masukkan nama file untuk menyimpan gambar (misalnya, frame_1.png):")

        if st.button("Simpan Gambar", key='button-style'):
            if save_path and file_name:
                full_path = os.path.join(save_path, file_name)
                image.save(full_path)
                st.write(f"Gambar disimpan sebagai {full_path}")
            else:
                st.write("Harap masukkan path direktori dan nama file yang valid.")

    cap.release()
