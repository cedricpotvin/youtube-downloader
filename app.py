import streamlit as st
from yt_dlp import YoutubeDL
import os

# Streamlit UI
st.title("YouTube Video Downloader 🎥")
st.markdown("Upload your YouTube cookies file and paste the video URL to download.")

# Upload cookies.txt
uploaded_file = st.file_uploader("Upload your cookies.txt file", type="txt")
if uploaded_file:
    with open("cookies.txt", "wb") as f:
        f.write(uploaded_file.getvalue())
    st.success("Cookies uploaded successfully!")

# Input YouTube URL
video_url = st.text_input("Enter YouTube URL:")

if st.button("Download"):
    if video_url:
        st.info("Processing your video (highest resolution available)...")
        try:
            # Ensure downloads directory exists
            download_dir = "downloads"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # yt-dlp options
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Best video+audio or best MP4
                'merge_output_format': 'mp4',  # Ensure final file is MP4
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Save to downloads directory
                'cookiefile': 'cookies.txt',  # Use cookies.txt for authentication
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',  # Ensure final format is MP4
                }],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
                }
            }

            # Download video
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                downloaded_file = ydl.prepare_filename(info)  # Get the actual file path

            # Check if the file exists and offer a download
            if os.path.exists(downloaded_file):
                st.success(f"Downloaded: {info.get('title', 'video')}")
                with open(downloaded_file, "rb") as file:
                    st.download_button(
                        label="Download Video (MP4)",
                        data=file,
                        file_name=os.path.basename(downloaded_file),
                        mime="video/mp4",
                    )
            else:
                st.error("The file could not be found after downloading. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
