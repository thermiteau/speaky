"""Tests for main module."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
import sys
from io import StringIO

from speaky.main import parse_arguments, main, cli_main


class TestParseArguments:
    """Tests for parse_arguments function."""
    
    def test_parse_arguments_with_text(self):
        """Test parsing arguments with text."""
        # Setup
        test_args = ["speaky", "hello", "world", "test"]
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
        
        # Verify
        assert args.text == ["hello", "world", "test"]
        assert not args.clear_cache
    
    def test_parse_arguments_no_text(self):
        """Test parsing arguments without text."""
        # Setup
        test_args = ["speaky"]
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
        
        # Verify
        assert args.text == []
        assert not args.clear_cache
    
    def test_parse_arguments_clear_cache(self):
        """Test parsing arguments with clear cache flag."""
        # Setup
        test_args = ["speaky", "--clear-cache"]
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
        
        # Verify
        assert args.clear_cache
        assert args.text == []
    
    def test_parse_arguments_clear_cache_with_text(self):
        """Test parsing arguments with both clear cache and text."""
        # Setup
        test_args = ["speaky", "--clear-cache", "hello", "world"]
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
        
        # Verify
        assert args.clear_cache
        assert args.text == ["hello", "world"]


class TestMain:
    """Tests for main function."""
    
    @patch('speaky.main.clear_cache')
    @patch('speaky.main.parse_arguments')
    @pytest.mark.asyncio
    async def test_main_clear_cache(self, mock_parse_args, mock_clear_cache):
        """Test main function with clear cache option."""
        # Setup
        mock_args = MagicMock()
        mock_args.clear_cache = True
        mock_parse_args.return_value = mock_args
        
        # Execute
        await main()
        
        # Verify
        mock_clear_cache.assert_called_once()
    
    @patch('speaky.main.play_audio_file')
    @patch('speaky.main.generate_and_cache_audio')
    @patch('speaky.main.load_config')
    @patch('speaky.main.parse_arguments')
    @pytest.mark.asyncio
    async def test_main_with_text(self, mock_parse_args, mock_load_config, 
                                  mock_generate_audio, mock_play_audio):
        """Test main function with text input."""
        # Setup
        mock_args = MagicMock()
        mock_args.clear_cache = False
        mock_args.text = ["hello", "world"]
        mock_parse_args.return_value = mock_args
        
        mock_config = {"api_key": "test"}
        mock_load_config.return_value = mock_config
        
        cache_file = Path("/test/cache.mp3")
        mock_generate_audio.return_value = cache_file
        
        # Execute
        await main()
        
        # Verify
        mock_load_config.assert_called_once()
        mock_generate_audio.assert_called_once_with("hello world", mock_config)
        mock_play_audio.assert_called_once_with(cache_file)
    
    @patch('speaky.main.play_audio_file')
    @patch('speaky.main.generate_and_cache_audio')
    @patch('speaky.main.load_config')
    @patch('speaky.main.parse_arguments')
    @pytest.mark.asyncio
    async def test_main_no_text(self, mock_parse_args, mock_load_config, 
                               mock_generate_audio, mock_play_audio):
        """Test main function with no text input."""
        # Setup
        mock_args = MagicMock()
        mock_args.clear_cache = False
        mock_args.text = []
        mock_parse_args.return_value = mock_args
        
        mock_config = {"api_key": "test"}
        mock_load_config.return_value = mock_config
        
        cache_file = Path("/test/cache.mp3")
        mock_generate_audio.return_value = cache_file
        
        # Execute
        await main()
        
        # Verify
        mock_generate_audio.assert_called_once_with("What would you like me to say?", mock_config)
        mock_play_audio.assert_called_once_with(cache_file)
    
    @patch('speaky.main.parse_arguments')
    @pytest.mark.asyncio
    async def test_main_config_error(self, mock_parse_args):
        """Test main function with configuration error."""
        # Setup
        mock_args = MagicMock()
        mock_args.clear_cache = False
        mock_args.text = ["test"]
        mock_parse_args.return_value = mock_args
        
        with patch('speaky.main.load_config', side_effect=ValueError("Config error")):
            # Execute & Verify
            with pytest.raises(SystemExit) as exc_info:
                await main()
            
            assert exc_info.value.code == 1
    
    @patch('speaky.main.parse_arguments')
    @pytest.mark.asyncio
    async def test_main_import_error(self, mock_parse_args):
        """Test main function with import error."""
        # Setup
        mock_args = MagicMock()
        mock_args.clear_cache = False
        mock_args.text = ["test"]
        mock_parse_args.return_value = mock_args
        
        with patch('speaky.main.load_config', side_effect=ImportError("Import error")):
            # Execute & Verify
            with pytest.raises(SystemExit) as exc_info:
                await main()
            
            assert exc_info.value.code == 1
    
    @patch('speaky.main.parse_arguments')
    @pytest.mark.asyncio
    async def test_main_unexpected_error(self, mock_parse_args):
        """Test main function with unexpected error."""
        # Setup
        mock_args = MagicMock()
        mock_args.clear_cache = False
        mock_args.text = ["test"]
        mock_parse_args.return_value = mock_args
        
        with patch('speaky.main.load_config', side_effect=Exception("Unexpected error")):
            # Execute & Verify
            with pytest.raises(SystemExit) as exc_info:
                await main()
            
            assert exc_info.value.code == 1


class TestCliMain:
    """Tests for cli_main function."""
    
    @patch('speaky.main.asyncio.run')
    def test_cli_main_success(self, mock_asyncio_run):
        """Test cli_main function successful execution."""
        # Execute
        cli_main()
        
        # Verify
        mock_asyncio_run.assert_called_once()
    
    @patch('speaky.main.asyncio.run')
    def test_cli_main_keyboard_interrupt(self, mock_asyncio_run):
        """Test cli_main function with keyboard interrupt."""
        # Setup
        mock_asyncio_run.side_effect = KeyboardInterrupt()
        
        # Execute & Verify
        with pytest.raises(SystemExit) as exc_info:
            cli_main()
        
        assert exc_info.value.code == 1
    
    @patch('speaky.main.asyncio.run')
    def test_cli_main_other_exception(self, mock_asyncio_run):
        """Test cli_main function with other exceptions."""
        # Setup
        mock_asyncio_run.side_effect = Exception("Some error")
        
        # Execute & Verify - should not catch other exceptions
        with pytest.raises(Exception) as exc_info:
            cli_main()
        
        assert "Some error" in str(exc_info.value)


class TestIntegration:
    """Integration tests combining multiple components."""
    
    @patch('speaky.main.play_audio_file')
    @patch('speaky.main.generate_and_cache_audio')
    @patch('speaky.main.load_config')
    @pytest.mark.asyncio
    async def test_full_workflow_integration(self, mock_load_config, 
                                           mock_generate_audio, mock_play_audio):
        """Test full workflow integration."""
        # Setup
        mock_config = {
            "api_key": "test-key",
            "model": "gpt-4o-mini-tts",
            "voice": "nova",
            "instructions": "test instructions",
            "response_format": "mp3"
        }
        mock_load_config.return_value = mock_config
        
        cache_file = Path("/test/integration.mp3")
        mock_generate_audio.return_value = cache_file
        
        # Mock sys.argv for argument parsing
        test_args = ["speaky", "integration", "test", "text"]
        with patch.object(sys, 'argv', test_args):
            # Execute
            await main()
        
        # Verify full workflow
        mock_load_config.assert_called_once()
        mock_generate_audio.assert_called_once_with("integration test text", mock_config)
        mock_play_audio.assert_called_once_with(cache_file)