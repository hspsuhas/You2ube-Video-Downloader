import streamlit as st
from pytube import YouTube
from io import BytesIO
from pathlib import Path

st.set_page_config(
    page_title="YTDownload",
    page_icon="icon.png",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "# Youtube Video: Viewer | Downloader | Converter"
    }
)

st.sidebar.image("logo.png")

with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>YTDownload</h1>", unsafe_allow_html=True)
    st.write("<h3 style='text-align: center;'>➤ View YT video</h1>", unsafe_allow_html=True)
    st.write("<h3 style='text-align: center;'>➤ Download YT Vedio</h1>", unsafe_allow_html=True)
    st.write("<h3 style='text-align: center;'>➤ Convert YT Video to Audio</h1>", unsafe_allow_html=True)

@st.cache_data
def download(url, is_video=True, video_quality=None):
    buffer = BytesIO()
    youtube = YouTube(url)

    if is_video:
        video_stream = youtube.streams.filter(file_extension="mp4", resolution=video_quality).first()
        if not video_stream:
            st.warning("Selected video quality is not available. Falling back to the highest resolution.")
            video_stream = youtube.streams.get_highest_resolution()
        video_stream.stream_to_buffer(buffer)
        default_filename = video_stream.default_filename
    else:
        audio_stream = youtube.streams.get_audio_only()
        audio_stream.download(filename="temp_audio")
        default_filename = "temp_audio"

        with open("temp_audio", "rb") as audio_file:
            buffer.write(audio_file.read())

    return default_filename, buffer

def main():
    st.write("## Youtube Video Converter and Downloader")
    url = st.text_input("# Insert YouTube URL:")
    download_type = st.selectbox("Select Download Type", ("Video", "Audio"))

    if download_type == "Video":
        video_quality_options = ["1080p (Recommended)", "720p", "480p", "360p", "240p", "144p"]
        video_quality = st.selectbox("Select Video Quality", video_quality_options)
    else:
        audio_quality_options = ["320kbps (Recommended)", "256kbps", "128kbps"]
        audio_quality = st.selectbox("Select Audio Quality", audio_quality_options)

    if url:
        is_video = True if download_type == "Video" else False
        msg = "Downloading Video" if is_video else "Downloading Audio"

        with st.spinner(f"{msg} from YouTube..."):
            if is_video:
                video_quality = None if video_quality == "Highest Resolution" else video_quality
                default_filename, buffer = download(url, is_video, video_quality)
            else:
                default_filename, buffer = download(url, is_video, audio_quality)

        if is_video:
            show_video = st.button("Watch Video")
            if show_video:
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
