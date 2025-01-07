import streamlit as st
from yt_dlp import YoutubeDL
import os
import subprocess

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

            # yt-dlp options to download video and audio separately
            ydl_opts = {
                'format': 'bestvideo+bestaudio',  # Download best video and audio streams
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Save to downloads directory
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = info.get("title", "video")
                video_file = os.path.join(download_dir, f"{video_title}.mp4")
                video_stream = os.path.join(download_dir, f"{video_title}.fvideo")
                audio_stream = os.path.join(download_dir, f"{video_title}.faudio")

            # Debugging: Check downloaded files
            st.info(f"Downloaded video stream: {video_stream}")
            st.info(f"Downloaded audio stream: {audio_stream}")

            # Merging video and audio using FFmpeg
            merged_file = os.path.join(download_dir, f"{video_title}_HD.mp4")
            merge_command = [
                "ffmpeg", "-y", "-i", video_stream, "-i", audio_stream, "-c:v", "copy", "-c:a", "aac", merged_file
            ]
            subprocess.run(merge_command, check=True)

            # Provide download button
            if os.path.exists(merged_file):
                st.success(f"Downloaded in HD: {video_title}")
                with open(merged_file, "rb") as file:
                    st.download_button(
                        label="Download MP4",
                        data=file,
                        file_name=f"{video_title}_HD.mp4",
                        mime="video/mp4",
                    )
            else:
                st.error("The merging process failed. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
