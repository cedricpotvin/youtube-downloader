import streamlit as st
from yt_dlp import YoutubeDL
import os

# Streamlit UI
st.title("YouTube Video Downloader 🎥")
st.markdown("Paste a YouTube video link below to download it as an MP4.")

# Input URL
video_url = st.text_input("Enter YouTube URL:")

if st.button("Download"):
    if video_url:
        st.info("Processing your video...")
        try:
            # Ensure downloads are saved in a consistent directory
            download_dir = "downloads"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # yt-dlp options
            ydl_opts = {
                'format': 'best',  # Download best pre-merged format
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Save to downloads directory
            }

            # Download video
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = info.get("title", "video")
                video_file = os.path.join(download_dir, f"{video_title}.mp4")

            # Provide a download link to the user
            if os.path.exists(video_file):  # Ensure file exists
                st.success(f"Downloaded: {video_title}")
                with open(video_file, "rb") as file:
                    st.download_button(
                        label="Download MP4",
                        data=file,
                        file_name=f"{video_title}.mp4",
                        mime="video/mp4",
                    )
            else:
                st.error("The file could not be found after downloading. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
