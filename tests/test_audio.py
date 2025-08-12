"""Tests for audio module."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from speaky.audio import play_audio_file


class TestPlayAudioFile:
    """Tests for play_audio_file function."""
    
    @patch('speaky.audio.vlc')
    @patch('speaky.audio.time.sleep')
    def test_play_audio_file_success(self, mock_sleep, mock_vlc):
        """Test successful audio file playback."""
        # Setup
        mock_player = MagicMock()
        mock_vlc.MediaPlayer.return_value = mock_player
        mock_player.get_state.side_effect = [
            mock_vlc.State.Playing,
            mock_vlc.State.Playing,
            mock_vlc.State.Ended
        ]
        
        test_file = Path("/test/file.mp3")
        
        # Execute
        play_audio_file(test_file)
        
        # Verify
        mock_vlc.MediaPlayer.assert_called_once_with(str(test_file))
        mock_player.play.assert_called_once()
        mock_player.stop.assert_called_once()
        mock_player.release.assert_called_once()
        
        # Check sleep calls - initial wait + polling
        assert mock_sleep.call_count >= 2
        mock_sleep.assert_any_call(0.5)  # Initial wait
        mock_sleep.assert_any_call(0.1)  # Polling wait
    
    @patch('speaky.audio.vlc')
    @patch('speaky.audio.time.sleep')
    def test_play_audio_file_with_buffering(self, mock_sleep, mock_vlc):
        """Test audio playback with buffering state."""
        # Setup
        mock_player = MagicMock()
        mock_vlc.MediaPlayer.return_value = mock_player
        mock_player.get_state.side_effect = [
            mock_vlc.State.Opening,
            mock_vlc.State.Buffering,
            mock_vlc.State.Playing,
            mock_vlc.State.Ended
        ]
        
        # Execute
        play_audio_file("/test/file.mp3")
        
        # Verify - should wait through all states
        assert mock_player.get_state.call_count == 4
    
    @patch('speaky.audio.vlc')
    @patch('speaky.audio.time.sleep')
    def test_play_audio_file_immediate_end(self, mock_sleep, mock_vlc):
        """Test audio playback that ends immediately."""
        # Setup
        mock_player = MagicMock()
        mock_vlc.MediaPlayer.return_value = mock_player
        mock_player.get_state.return_value = mock_vlc.State.Ended
        
        # Execute
        play_audio_file("/test/file.mp3")
        
        # Verify
        mock_player.play.assert_called_once()
        mock_player.stop.assert_called_once()
        mock_player.release.assert_called_once()
        
        # Should only have initial sleep, no polling
        mock_sleep.assert_called_once_with(0.5)
    
    @patch('speaky.audio.vlc')
    @patch('speaky.audio.time.sleep')
    def test_play_audio_file_vlc_error(self, mock_sleep, mock_vlc):
        """Test audio playback with VLC error."""
        # Setup
        mock_vlc.MediaPlayer.side_effect = Exception("VLC error")
        
        # Execute & Verify
        with pytest.raises(Exception) as exc_info:
            play_audio_file("/test/file.mp3")
        
        assert "VLC error" in str(exc_info.value)
    
    @patch('speaky.audio.vlc')
    @patch('speaky.audio.time.sleep')
    def test_play_audio_file_player_error(self, mock_sleep, mock_vlc, capsys):
        """Test audio playback with player error."""
        # Setup
        mock_player = MagicMock()
        mock_vlc.MediaPlayer.return_value = mock_player
        mock_player.play.side_effect = Exception("Player error")
        
        # Execute & Verify
        with pytest.raises(Exception) as exc_info:
            play_audio_file("/test/file.mp3")
        
        # Check error message was printed
        captured = capsys.readouterr()
        assert "❌ Error playing audio: Player error" in captured.out
        assert "Make sure VLC is installed" in captured.out
    
    @patch('speaky.audio.vlc')
    @patch('speaky.audio.time.sleep')
    def test_play_audio_file_pathlib_path(self, mock_sleep, mock_vlc):
        """Test play_audio_file with pathlib Path object."""
        # Setup
        mock_player = MagicMock()
        mock_vlc.MediaPlayer.return_value = mock_player
        mock_player.get_state.return_value = mock_vlc.State.Ended
        
        test_path = Path("/test/file.mp3")
        
        # Execute
        play_audio_file(test_path)
        
        # Verify path is converted to string
        mock_vlc.MediaPlayer.assert_called_once_with(str(test_path))
    
    @patch('speaky.audio.vlc')
    @patch('speaky.audio.time.sleep')
    def test_play_audio_file_string_path(self, mock_sleep, mock_vlc):
        """Test play_audio_file with string path."""
        # Setup
        mock_player = MagicMock()
        mock_vlc.MediaPlayer.return_value = mock_player
        mock_player.get_state.return_value = mock_vlc.State.Ended
        
        test_path = "/test/file.mp3"
        
        # Execute
        play_audio_file(test_path)
        
        # Verify
        mock_vlc.MediaPlayer.assert_called_once_with(test_path)