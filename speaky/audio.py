"""Audio playback functionality."""

import time
import vlc

 
def play_audio_file(file_path):
    """Play audio file using VLC."""
    try:
        player = vlc.MediaPlayer(str(file_path))
        player.play()
        
        # Wait for playback to start
        time.sleep(0.5)
        
        # Wait for playback to finish
        while player.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
            time.sleep(0.1)
        
        player.stop()
        player.release()
    except Exception as e:
        print(f"❌ Error playing audio: {e}")
        print("Make sure VLC is installed on your system.")
        raise