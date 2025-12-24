import streamlit as st
import yt_dlp
import tempfile
import os

st.set_page_config(
    page_title="Facebook Video Downloader",
    layout="centered"
)

st.title("Facebook Video Downloader")

url = st.text_input("URL del video de Facebook")

quality = st.selectbox(
    "Calidad del video",
    ["Mejor disponible", "720p", "480p"]
)

def get_format(quality):
    if quality == "720p":
        return "bestvideo[height<=720]+bestaudio/best"
    elif quality == "480p":
        return "bestvideo[height<=480]+bestaudio/best"
    return "best"

if st.button("Descargar"):
    if not url:
        st.warning("Pega una URL válida.")
    else:
        with st.spinner("Procesando video..."):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    ydl_opts = {
                        "outtmpl": f"{temp_dir}/%(title)s.%(ext)s",
                        "format": get_format(quality),
                        "merge_output_format": "mp4",
                        "quiet": True
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)

                    with open(filename, "rb") as file:
                        st.success("Video listo para descargar.")
                        st.download_button(
                            label="Descargar en mi dispositivo",
                            data=file,
                            file_name=os.path.basename(filename),
                            mime="video/mp4"
                        )

            except Exception as e:
                st.error("No se pudo descargar el video.")
                st.exception(e)
