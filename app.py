import streamlit as st
from yt_dlp import YoutubeDL
import os

st.title("YouTube Video Downloader 🎥")
st.markdown("Upload your YouTube cookies file and paste the video URL to download.")

uploaded_file = st.file_uploader("Upload your cookies.txt file", type="txt")
if uploaded_file:
    with open("cookies.txt", "wb") as f:
        f.write(uploaded_file.getvalue())
    st.success("Cookies uploaded successfully!")

video_url = st.text_input("Enter YouTube URL:")

if st.button("Download"):
    if video_url:
        st.info("Processing your video (highest resolution available)...")
        try:
            download_dir = "downloads"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                'cookiefile': 'cookies.txt',
                'postprocessors': [{
                    'key': 'FFmpegMerger',
                }],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
                }
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                merged_file_path = ydl.prepare_filename(info).replace(".f398", "").replace(".f140", "")  # Ensure correct path

            # Debug: Verify merged file
            print("Files in downloads directory:", os.listdir(download_dir))
            if not os.path.exists(merged_file_path):
                st.error("Merged file not found. Check logs for details.")
            else:
                st.success(f"Downloaded: {info.get('title', 'video')}")
                with open(merged_file_path, "rb") as file:
                    st.download_button(
                        label="Download Video (MP4)",
                        data=file,
                        file_name=os.path.basename(merged_file_path),
                        mime="video/mp4",
                    )
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide a valid YouTube URL.")
