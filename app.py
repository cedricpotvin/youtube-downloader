import streamlit as st
from yt_dlp import YoutubeDL
import os

# Streamlit UI
st.title("YouTube Video Downloader 🎥")
st.markdown("Paste a YouTube video link below to download it in the highest quality.")

# Input URL
video_url = st.text_input("Enter YouTube URL:")

if st.button("Download"):
    if video_url:
        st.info("Processing your video in the highest quality...")
        try:
            # Ensure downloads are saved in a consistent directory
            download_dir = "downloads"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # yt-dlp options for highest quality
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',  # Download best video and audio separately, then merge
                'merge_output_format': 'mp4',  # Output as MP4 after merging
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Save to downloads directory
                'postprocessors': [
                    {  # Merges video and audio using FFmpeg (handled internally by yt-dlp)
                        'key': 'FFmpegMerger',
                    }
                ],
            }

            # Download video
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_file = os.path.join(download_dir, f"{info.get('title', 'video')}.mp4")

            # Provide download button
            if os.path.exists(video_file):
                st.success(f"Downloaded: {info.get('title', 'video')}")
                with open(video_file, "rb") as file:
                    st.download_button(
                        label="Download MP4",
                        data=file,
                        file_name=os.path.basename(video_file),
                        mime="video/mp4",
                    )
            else:
                st.error("The file could not be found after downloading. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
