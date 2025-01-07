import streamlit as st
from yt_dlp import YoutubeDL
import os

# Streamlit UI
st.title("YouTube Video Downloader 🎥")
st.markdown("Paste a YouTube video link below to download it in HD quality.")

# Input URL
video_url = st.text_input("Enter YouTube URL:")

if st.button("Download"):
    if video_url:
        st.info("Processing your video in HD quality...")
        try:
            # Ensure downloads are saved in a consistent directory
            download_dir = "downloads"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # yt-dlp options for highest-quality video and audio
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',  # Ensure highest video and audio quality
                'merge_output_format': 'mp4',  # Output as MP4
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Save to downloads directory
                'postprocessors': [
                    {  # Merge video and audio into one file
                        'key': 'FFmpegMerger',
                    }
                ],
            }

            # Download video
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = info.get("title", "video")
                output_file = os.path.join(download_dir, f"{video_title}.mp4")

            # Check if merged file exists
            if os.path.exists(output_file):
                st.success(f"Downloaded in HD: {video_title}")
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="Download MP4",
                        data=file,
                        file_name=f"{video_title}.mp4",
                        mime="video/mp4",
                    )
            else:
                st.error("The merging process failed or the file was not found. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
