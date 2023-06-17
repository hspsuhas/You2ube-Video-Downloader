import streamlit as st
from pytube import YouTube
from io import BytesIO
from pathlib import Path

st.set_page_config(
    page_title="YTDownload",
    page_icon="📹",
)

@st.cache_data
def download(url, is_video=True):
    buffer = BytesIO()
    youtube = YouTube(url)
    if is_video:
        media = youtube.streams.get_highest_resolution() 
    else:
        media = youtube.streams.get_audio_only()
    default_filename = media.default_filename
    media.stream_to_buffer(buffer)
    return default_filename, buffer

def main():
    st.title("Youtube Vedio Converter and Downloader")
    url = st.text_input("# Insert YouTube URL:")
    download_type = st.selectbox("Select Download Type", ("Video", "Audio"))

    if url:
        is_video = True if download_type == "Video" else False
        msg = "Downloading Vedio"
        if not is_video:
            msg = "Converting Video to Audio"
        with st.spinner(f"{msg} from YouTube..."):
            default_filename, buffer = download(url, is_video)

        if is_video:
            st.subheader("Watch Video")
            st.video(buffer)
        else:
            st.subheader("Listen to Audio")
            st.audio(buffer, format="audio/mpeg")

        st.subheader("Download File")
        st.download_button(
            label=f"Download {download_type.lower()}",
            data=buffer,
            file_name=Path(default_filename).name,
            mime="video/mp4" if is_video else "audio/mpeg",
        )

if __name__ == "__main__":
    main()
