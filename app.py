import streamlit as st
from yt_dlp import YoutubeDL

# Streamlit UI
st.title("YouTube Video Downloader 🎥")
st.markdown("Paste a YouTube video link below to download it as an MP4.")

# Input URL
video_url = st.text_input("Enter YouTube URL:")

if st.button("Download"):
    if video_url:
        st.info("Processing your video...")
        try:
            # Use yt-dlp to download the best merged format
            ydl_opts = {
                'format': 'best',  # Download the best available format already merged
                'outtmpl': '%(title)s.%(ext)s',  # Save file with the video title as filename
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = info.get("title", "video")
                video_file = f"{video_title}.mp4"

            # Provide download link
            st.success(f"Downloaded: {video_title}")
            with open(video_file, "rb") as file:
                st.download_button(
                    label="Download MP4",
                    data=file,
                    file_name=video_file,
                    mime="video/mp4",
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
