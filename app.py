import streamlit as st
from yt_dlp import YoutubeDL
import ffmpeg
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
            # Step 1: Download video and audio separately
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'outtmpl': '%(title)s.%(ext)s',
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = info.get("title", "video")
                video_file = f"{video_title}.mp4"
                audio_file = f"{video_title}.m4a"

            # Step 2: Merge video and audio using ffmpeg-python
            output_file = f"{video_title}_merged.mp4"
            ffmpeg.input(video_file).output(audio_file, vcodec="copy", acodec="aac").output(output_file).run()

            # Step 3: Provide download link
            st.success(f"Downloaded and merged: {output_file}")
            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download MP4",
                    data=file,
                    file_name=output_file,
                    mime="video/mp4",
                )

            # Clean up intermediate files
            os.remove(video_file)
            os.remove(audio_file)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
