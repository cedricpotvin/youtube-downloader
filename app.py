import streamlit as st
from yt_dlp import YoutubeDL
import ffmpeg

# Streamlit UI
st.title("YouTube Video Downloader 🎥")
st.markdown("Paste a YouTube video link below to download it as an MP4.")

# Input URL
video_url = st.text_input("Enter YouTube URL:")

if st.button("Download"):
    if video_url:
        st.info("Processing your video...")
        try:
            # Set yt-dlp options to avoid direct merging
            ydl_opts = {
                'format': 'bestvideo+bestaudio',
                'outtmpl': '%(title)s.%(ext)s',
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = info.get("title", "video")
                video_filename = f"{video_title}.mp4"

            # Merge video and audio using ffmpeg-python
            video_stream = ffmpeg.input(f"{video_title}.fvideo")
            audio_stream = ffmpeg.input(f"{video_title}.faudio")
            ffmpeg.output(video_stream, audio_stream, video_filename).run()

            # Provide download link
            st.success(f"Downloaded: {video_title}")
            with open(video_filename, "rb") as file:
                st.download_button(
                    label="Download MP4",
                    data=file,
                    file_name=video_filename,
                    mime="video/mp4",
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
