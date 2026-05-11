import os
import subprocess
import sys

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: ffmpeg is not installed or not found in PATH.")
        print("Install it via: https://ffmpeg.org/download.html")
        sys.exit(1)

def convert_folder(folder_num, base_dir):
    folder_path = os.path.join(base_dir, str(folder_num))

    if not os.path.isdir(folder_path):
        print(f"  [{folder_num}] Skipping — folder not found.")
        return

    vid_path   = os.path.join(folder_path, "vid.mp4")
    bg_path    = os.path.join(folder_path, "bg.mp4")
    track_path = os.path.join(folder_path, "track.mp3")

    if not os.path.isfile(vid_path):
        print(f"  [{folder_num}] Skipping — vid.mp4 not found.")
        return

    print(f"  [{folder_num}] Processing {vid_path} ...")

    # bg.mp4 : video, no audio
    print(f"         -> bg.mp4 (video)")
    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", vid_path,
            "-an",            # strip audio
            "-c:v", "copy",   # copy video stream as-is (fast)
            bg_path,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"         ERROR creating bg.mp4:\n{result.stderr}")
    else:
        print(f"         ✓ bg.mp4 saved.")

    # track.mp3 : audio, 44100 Hz
    print(f"         -> track.mp3 (audio, 44100 Hz)")
    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", vid_path,
            "-vn", # strip video
            "-ar", "44100", # sample rate
            "-ac", "2", # stereo
            "-q:a", "2", # VBR quality (≈190 kbps)
            track_path,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"         ERROR creating track.mp3:\n{result.stderr}")
    else:
        print(f"         + track.mp3 saved.")

def main():
    # same folder as this script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 50)
    print("  vid.mp4 → bg.mp4 + track.mp3 converter")
    print("=" * 50)
    print(f"Base directory : {base_dir}")
    print(f"Scanning folders: 2 – 29\n")

    check_ffmpeg()

    for num in range(2, 30): # 2 inclusive … 29 inclusive
        convert_folder(num, base_dir)

    print("\nDone!")


if __name__ == "__main__":
    main()