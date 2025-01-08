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
                'format': 'bestvideo+bestaudio/best',  # Best video+audio or best single format
                'merge_output_format': 'mp4',  # Final merged output as MP4
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Save to downloads directory
                'cookiefile': 'cookies.txt',  # Use cookies.txt for authentication
                'postprocessors': [{
                    'key': 'FFmpegMerger',  # Merge video and audio
                }],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
                }
            }

            # Download video
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)

            # Handle the merged file
            merged_file_path = os.path.join(download_dir, f"{info['title']}.mp4")
            print(f"Looking for merged file: {merged_file_path}")
            if os.path.exists(merged_file_path):
                st.success(f"Downloaded: {info['title']}")
                with open(merged_file_path, "rb") as file:
                    st.download_button(
                        label="Download Video (MP4)",
                        data=file,
                        file_name=os.path.basename(merged_file_path),
                        mime="video/mp4",
                    )
            else:
                st.error("Merged file not found. Please check logs for details.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error(f"Detailed error: {str(e)}")  # Log the specific error for debugging
    else:
        st.warning("Please provide a valid YouTube URL.")
