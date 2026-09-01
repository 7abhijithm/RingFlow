import os
import re
import subprocess
import requests
import static_ffmpeg
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, error

# Ensure static ffmpeg binaries are discovered
static_ffmpeg.add_paths()

def sanitize_filename(name: str) -> str:
    """Strip illegal filesystem characters."""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def process_youtube_ringtone(url: str):
    print(f"\n[1/4] Fetching metadata and downloading audio from YouTube...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_raw.%(ext)s',
        'writethumbnail': True,
        'quiet': False,
        'no_warnings': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        raw_title = info.get('title', 'Ringtone')
        safe_title = sanitize_filename(raw_title)
        thumbnail_url = info.get('thumbnail')
        raw_ext = info.get('ext', 'webm')
        raw_filename = f"temp_raw.{raw_ext}"

    thumb_filename = "temp_thumb.jpg"
    if thumbnail_url:
        try:
            resp = requests.get(thumbnail_url, timeout=15)
            if resp.status_code == 200:
                with open(thumb_filename, "wb") as f:
                    f.write(resp.content)
        except Exception as e:
            print(f"Warning: Could not download thumbnail ({e})")

    print(f"\n[2/4] Processing track: {safe_title}")

    # Standard EBU R128 loudness normalization for crisp phone speaker output
    af_filters = "loudnorm=I=-16:TP=-1.5:LRA=11"

    mp3_out = f"{safe_title}_HQ.mp3"
    m4r_out = f"{safe_title}_HQ.m4r"

    # 1. Export HQ MP3 (Android)
    print("\n[3/4] Exporting MP3 (320kbps) with embedded cover art...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", raw_filename,
        "-af", af_filters,
        "-b:a", "320k",
        "-ar", "48000",
        mp3_out
    ], check=True)

    # Embed Cover Art into MP3 ID3 Tags
    if os.path.exists(thumb_filename):
        try:
            audio_file = MP3(mp3_out, ID3=ID3)
            try:
                audio_file.add_tags()
            except error:
                pass
            with open(thumb_filename, "rb") as albumart:
                audio_file.tags.add(
                    APIC(
                        encoding=3,
                        mime="image/jpeg",
                        type=3,
                        desc="Cover",
                        data=albumart.read()
                    )
                )
            audio_file.tags.add(TIT2(encoding=3, text=raw_title))
            audio_file.save()
        except Exception as e:
            print(f"Warning: Could not embed ID3 thumbnail ({e})")

    # 2. Export HQ M4R with embedded cover art (iPhone)
    print("\n[4/4] Exporting M4R (256kbps AAC)...")
    m4r_cmd = [
        "ffmpeg", "-y",
        "-i", raw_filename
    ]
    if os.path.exists(thumb_filename):
        m4r_cmd.extend(["-i", thumb_filename, "-map", "0:a", "-map", "1:v", "-c:v", "mjpeg", "-disposition:v", "attached_pic"])
    
    m4r_cmd.extend([
        "-af", af_filters,
        "-c:a", "aac",
        "-b:a", "256k",
        "-ar", "48000",
        "-f", "ipod",
        m4r_out
    ])
    subprocess.run(m4r_cmd, check=True)

    # Clean temporary files
    for temp in [raw_filename, thumb_filename, "temp_raw.webm", "temp_raw.m4a", "temp_raw.opus"]:
        if os.path.exists(temp):
            try:
                os.remove(temp)
            except OSError:
                pass

    print("\n" + "=" * 55)
    print("✨ Ringtone generation successful!")
    print(f" • Android File: {mp3_out}")
    print(f" • iPhone File:  {m4r_out}")
    print("=" * 55)

def main():
    print("=" * 55)
    print("          RingFlow - YouTube Ringtone Maker         ")
    print("=" * 55)
    while True:
        url = input("\nEnter YouTube URL (or press Enter to exit): ").strip()
        if not url:
            break
        try:
            process_youtube_ringtone(url)
        except Exception as e:
            print(f"\n❌ Error processing URL: {e}")

if __name__ == "__main__":
    main()