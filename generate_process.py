# This file looks for new folders inside user uploads and converts them to reel if they are not already converted
import os
from text_to_audio import text_to_speech_file
import time
import subprocess


def text_to_audio(folder):
    print("TTA - ", folder)
    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()
    print(text, folder)
    if not text or not text.strip():
        print(
            f"No description provided for folder={folder}; skipping TTS and using fallback audio")
        return
    try:
        text_to_speech_file(text, folder)
    except Exception as e:
        print(f"text_to_speech_file failed for folder={folder}:", e)


def create_reel(folder):
    out_dir = os.path.join("static", "reels")
    os.makedirs(out_dir, exist_ok=True)

    folder_path = os.path.join("user_uploads", folder)
    audio_path = os.path.join(folder_path, "audio.mp3")
    need_fallback = False
    if not os.path.exists(audio_path):
        need_fallback = True
        reason = "missing"
    else:
        try:
            if os.path.getsize(audio_path) < 1024:
                need_fallback = True
                reason = "size too small"
        except Exception:
            need_fallback = True
            reason = "stat-failed"

    if need_fallback:
        default_song = os.path.join("static", "songs", "1.mp3")
        if not os.path.exists(default_song):
            print(
                f"Default song not found at {default_song}; cannot fallback for folder={folder}")
        else:
            try:
                with open(default_song, "rb") as src, open(audio_path, "wb") as dst:
                    dst.write(src.read())
                print(
                    f"Copied default song to {audio_path} (reason: {reason})")
            except Exception as e:
                print(f"Failed to copy default song for folder={folder}:", e)
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "input.txt",
        "-i", "audio.mp3",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        os.path.abspath(os.path.join(out_dir, f"{folder}.mp4")),
    ]

    try:
        subprocess.run(cmd, cwd=folder_path, check=True)
        print("CR - ", folder)
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg failed for folder={folder} returncode={e.returncode}")
        print("cmd:", " ".join(cmd))
    except Exception as e:
        print("Unexpected exception while running ffmpeg:", e)


if __name__ == "__main__":
    while True:
        print("Processing queue...")
        with open("done.txt", "r") as f:
            done_folders = f.readlines()

        done_folders = [f.strip() for f in done_folders]
        folders = os.listdir("user_uploads")
        for folder in folders:
            if (folder not in done_folders):
                # Generate the audio.mp3 from desc.txt (may fail)
                text_to_audio(folder)
                audio_path = os.path.join("user_uploads", folder, "audio.mp3")
                need_fallback = False
                if not os.path.exists(audio_path):
                    need_fallback = True
                    reason = "missing"
                else:
                    try:
                        size = os.path.getsize(audio_path)
                        if size < 1024:
                            need_fallback = True
                            reason = f"size {size} bytes too small"
                    except Exception:
                        need_fallback = True
                        reason = "stat-failed"

                if need_fallback:
                    default_song = os.path.join("static", "songs", "1.mp3")
                    try:
                        if not os.path.exists(default_song):
                            print(
                                f"Default song not found at {default_song}; cannot fallback")
                        else:
                            with open(default_song, "rb") as src, open(audio_path, "wb") as dst:
                                dst.write(src.read())
                            print(
                                f"Copied default song to {audio_path} (reason: {reason})")
                    except Exception as e:
                        print(
                            f"Failed to copy default song for folder={folder}:", e)

                create_reel(folder)
                with open("done.txt", "a") as f:
                    f.write(folder + "\n")
        time.sleep(4)
