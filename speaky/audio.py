"""Audio playback functionality."""

from __future__ import annotations

import time
from pathlib import Path

import vlc


def play_audio_file(file_path: str | Path) -> None:
    """Play audio file using VLC."""
    try:
        player = vlc.MediaPlayer(str(file_path))
        if player is None:
            raise RuntimeError("Failed to initialize VLC media player")
        player.play()

        # Wait for playback to start
        time.sleep(0.5)

        # Wait for playback to finish
        while player.get_state() in [
            vlc.State.Playing,  # type: ignore
            vlc.State.Opening,  # type: ignore
            vlc.State.Buffering,  # type: ignore
        ]:
            time.sleep(0.1)

        player.stop()
        player.release()
    except Exception as e:
        print(f"❌ Error playing audio: {e}")
        print("Make sure VLC is installed on your system.")
        raise
