import os
import re
from bs4 import BeautifulSoup
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip

# Function to extract YouTube URLs from an HTML file


def extract_youtube_urls(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    thumbnails = soup.find_all('a', {'id': 'thumbnail'})
    urls = []

    # Extract unique YouTube URLs
    for thumbnail in thumbnails:
        href = thumbnail.get('href')
        if href and '/watch?v=' in href:
            urls.append("https://www.youtube.com" + href)

    # Remove duplicates
    urls = list(set(urls))
    return urls

# Function to extract YouTube URLs using regex (alternative method)


def extract_youtube_urls_regex(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Regex pattern to find URLs
    pattern = r'"url":\s*"(/watch\?v=[^"]+)"'
    matches = re.findall(pattern, html)

    # Generate complete URLs
    urls = ["https://www.youtube.com" + match for match in matches]
    return list(set(urls))

# Function to download videos from YouTube


def download_youtube_videos(urls, download_folder="./videos"):
    failed = []

    # Create folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for url in urls:
        try:
            yt = YouTube(url)
            best_video_stream = yt.streams.get_highest_resolution()
            best_video_stream.download(output_path=download_folder)
            print(f"Downloaded: {url}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            failed.append(url)

    return failed

# Function to convert MP4 files to MP3  (requires moviepy library)


def convert_mp4_to_mp3(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = os.listdir(input_folder)

    for file in files:
        if file.endswith(".mp4"):
            input_path = os.path.join(input_folder, file)
            output_file = os.path.splitext(file)[0] + ".mp3"
            output_path = os.path.join(output_folder, output_file)

            try:
                video_clip = VideoFileClip(input_path)
                audio_clip = video_clip.audio
                audio_clip.write_audiofile(output_path, codec='mp3')
                print(f"Converted: {file} to MP3")

                # Close clips
                audio_clip.close()
                video_clip.close()
            except Exception as e:
                print(f"Error converting {file}: {e}")


if __name__ == "__main__":
    # Extract YouTube URLs from the HTML file
    html_file = './youtube.html'
    urls = extract_youtube_urls(html_file)

    # Optionally, you can use the regex-based extractor:
    # urls = extract_youtube_urls_regex(html_file)

    # Save URLs to file
    with open('urls.txt', 'w') as f:
        for url in urls:
            f.write(url + '\n')

    # Download the YouTube videos
    failed_downloads = download_youtube_videos(urls)

    # Optionally, save failed downloads to a file
    if failed_downloads:
        with open('failed_urls.txt', 'w') as f:
            for url in failed_downloads:
                f.write(url + '\n')

    # Convert downloaded MP4 videos to MP3
    input_folder = "./videos/"
    output_folder = "./mp3/"
    convert_mp4_to_mp3(input_folder, output_folder)
