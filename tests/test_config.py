"""Tests for config module."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from speaky.config import get_cache_dir, load_config, install_default_config, DEFAULT_CONFIG


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
    @patch('speaky.config.USER_CONFIG_PATH', Path("/nonexistent/.speaky.json"))
    @patch('speaky.config.load_dotenv')
    def test_load_config_defaults(self, mock_load_dotenv):
        """Test configuration loading with defaults when no user config exists."""
        config = load_config()

        expected_config = {
            "api_key": "test-api-key",
            "model": "gpt-4o-mini-tts",
            "voice": "nova",
            "instructions": "Speak in a cheerful, positive yet professional tone.",
            "response_format": "mp3"
        }
        assert config == expected_config
        mock_load_dotenv.assert_called_once()

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    @patch('speaky.config.load_dotenv')
    def test_load_config_user_overrides(self, mock_load_dotenv):
        """Test that user config overrides defaults."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"voice": "alloy", "model": "tts-1"}, f)
            tmp_path = Path(f.name)

        try:
            with patch('speaky.config.USER_CONFIG_PATH', tmp_path):
                config = load_config()

            assert config["voice"] == "alloy"
            assert config["model"] == "tts-1"
            assert config["instructions"] == DEFAULT_CONFIG["instructions"]
            assert config["api_key"] == "test-api-key"
        finally:
            tmp_path.unlink()
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('speaky.config.USER_CONFIG_PATH', Path("/nonexistent/.speaky.json"))
    @patch('speaky.config.load_dotenv')
    def test_load_config_missing_api_key(self, mock_load_dotenv):
        """Test configuration loading fails with missing API key."""
        with pytest.raises(ValueError) as exc_info:
            load_config()

        assert "OPENAI_API_KEY not found" in str(exc_info.value)
        mock_load_dotenv.assert_called_once()

    @patch.dict(os.environ, {'OPENAI_API_KEY': ''})
    @patch('speaky.config.USER_CONFIG_PATH', Path("/nonexistent/.speaky.json"))
    @patch('speaky.config.load_dotenv')
    def test_load_config_empty_api_key(self, mock_load_dotenv):
        """Test configuration loading fails with empty API key."""
        with pytest.raises(ValueError) as exc_info:
            load_config()

        assert "OPENAI_API_KEY not found" in str(exc_info.value)


class TestInstallDefaultConfig:
    """Tests for install_default_config function."""

    def test_creates_config_when_missing(self):
        """Test that default config is created when it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / ".speaky.json"
            with patch('speaky.config.USER_CONFIG_PATH', config_path):
                install_default_config()

            assert config_path.exists()
            written = json.loads(config_path.read_text())
            assert written == DEFAULT_CONFIG

    def test_does_not_overwrite_existing(self):
        """Test that existing config is not overwritten."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            custom = {"voice": "echo"}
            json.dump(custom, f)
            config_path = Path(f.name)

        try:
            with patch('speaky.config.USER_CONFIG_PATH', config_path):
                install_default_config()

            written = json.loads(config_path.read_text())
            assert written == custom
        finally:
            config_path.unlink()