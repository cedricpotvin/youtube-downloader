import streamlit as st
from yt_dlp import YoutubeDL
import os

# Streamlit UI
st.title("YouTube Video Downloader 🎥")
st.markdown("Paste a YouTube video link below to download the highest-resolution video (without audio).")

# Input URL
video_url = st.text_input("Enter YouTube URL:")

if st.button("Download"):
    if video_url:
        st.info("Processing your video (highest resolution, video only)...")
        try:
            # Ensure downloads are saved in a consistent directory
            download_dir = "downloads"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # yt-dlp options for highest resolution video
            ydl_opts = {
                'format': 'bestvideo[height>=1080]',  # Prefer 1080p or higher video streams
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Save to downloads directory
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                downloaded_file = ydl.prepare_filename(info)  # Dynamically get the actual filename
                st.info(f"Downloaded file path: {downloaded_file}")  # Debugging message

            # Check if the file exists
            if os.path.exists(downloaded_file):
                st.success(f"Downloaded (HD Video Only): {info.get('title', 'video')}")
                with open(downloaded_file, "rb") as file:
                    st.download_button(
                        label="Download Video (MP4)",
                        data=file,
                        file_name=os.path.basename(downloaded_file),
                        mime="video/mp4",
                    )
            else:
                st.error("The file could not be found after downloading. Please check for any issues with the URL or file name.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
