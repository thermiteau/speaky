"""Tests for config module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from speaky.config import get_cache_dir, load_config


class TestGetCacheDir:
    """Tests for get_cache_dir function."""
    
    @patch('speaky.config.platformdirs')
    def test_get_cache_dir_creates_directory(self, mock_platformdirs):
        """Test that get_cache_dir creates the cache directory."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "speaky"
            mock_platformdirs.user_cache_dir.return_value = str(cache_path)
            
            # Execute
            result = get_cache_dir()
            
            # Verify
            assert result == cache_path
            assert cache_path.exists()
            mock_platformdirs.user_cache_dir.assert_called_once_with("speaky")
    
    @patch('speaky.config.platformdirs')
    def test_get_cache_dir_existing_directory(self, mock_platformdirs):
        """Test that get_cache_dir works with existing directory."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "speaky"
            cache_path.mkdir(parents=True, exist_ok=True)
            mock_platformdirs.user_cache_dir.return_value = str(cache_path)
            
            # Execute
            result = get_cache_dir()
            
            # Verify
            assert result == cache_path
            assert cache_path.exists()


class TestLoadConfig:
    """Tests for load_config function."""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('speaky.config.load_dotenv')
    def test_load_config_success(self, mock_load_dotenv):
        """Test successful configuration loading."""
        # Execute
        config = load_config()
        
        # Verify
        expected_config = {
            "api_key": "test-api-key",
            "model": "gpt-4o-mini-tts",
            "voice": "nova",
            "instructions": "Speak in a cheerful, positive yet professional tone.",
            "response_format": "mp3"
        }
        assert config == expected_config
        mock_load_dotenv.assert_called_once()
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('speaky.config.load_dotenv')
    def test_load_config_missing_api_key(self, mock_load_dotenv):
        """Test configuration loading fails with missing API key."""
        # Execute & Verify
        with pytest.raises(ValueError) as exc_info:
            load_config()
        
        assert "OPENAI_API_KEY not found" in str(exc_info.value)
        mock_load_dotenv.assert_called_once()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': ''})
    @patch('speaky.config.load_dotenv')
    def test_load_config_empty_api_key(self, mock_load_dotenv):
        """Test configuration loading fails with empty API key."""
        # Execute & Verify
        with pytest.raises(ValueError) as exc_info:
            load_config()
        
        assert "OPENAI_API_KEY not found" in str(exc_info.value)