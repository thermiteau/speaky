"""Tests for TTS module."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from unittest.mock import AsyncMock
from contextlib import asynccontextmanager

from speaky.tts import generate_and_cache_audio


class TestGenerateAndCacheAudio:
    """Tests for generate_and_cache_audio function."""
    
    @patch('speaky.tts.get_cache_file')
    @pytest.mark.asyncio
    async def test_generate_and_cache_audio_cached_file_exists(self, mock_get_cache_file):
        """Test function returns existing cached file without API call."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_file = Path(temp_dir) / "cached.mp3"
            cache_file.touch()  # Create the file
            mock_get_cache_file.return_value = cache_file
            
            config = {
                "api_key": "test-key",
                "model": "gpt-4o-mini-tts",
                "voice": "nova",
                "instructions": "test instructions",
                "response_format": "mp3"
            }
            
            # Execute
            result = await generate_and_cache_audio("test text", config)
            
            # Verify
            assert result == cache_file
            mock_get_cache_file.assert_called_once_with(
                "test text", "nova", "test instructions"
            )
    
    @patch('speaky.tts.AsyncOpenAI')
    @patch('speaky.tts.get_cache_file')
    @pytest.mark.asyncio
    async def test_generate_and_cache_audio_new_file(self, mock_get_cache_file, mock_openai_class):
        """Test function generates new audio file via API."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_file = Path(temp_dir) / "new.mp3"
            mock_get_cache_file.return_value = cache_file
            
            # Mock OpenAI client and response
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client
            
            # Create mock response with async iterator
            mock_response = AsyncMock()
            
            async def mock_async_iter():
                for chunk in [b'audio', b'data', b'chunks']:
                    yield chunk
            
            mock_response.iter_bytes = mock_async_iter
            
            # Create proper async context manager
            @asynccontextmanager
            async def mock_context_manager(*args, **kwargs):
                yield mock_response
            
            mock_client.audio.speech.with_streaming_response.create = mock_context_manager
            
            config = {
                "api_key": "test-key",
                "model": "gpt-4o-mini-tts",
                "voice": "nova",
                "instructions": "test instructions",
                "response_format": "mp3"
            }
            
            # Execute
            result = await generate_and_cache_audio("test text", config)
            
            # Verify
            assert result == cache_file
            assert cache_file.exists()
            
            # Check OpenAI client was created with correct API key
            mock_openai_class.assert_called_once_with(api_key="test-key")
            
            # Check file content
            with open(cache_file, 'rb') as f:
                content = f.read()
            assert content == b'audiodatachunks'
    
    @patch('speaky.tts.AsyncOpenAI')
    @patch('speaky.tts.get_cache_file')
    @pytest.mark.asyncio
    async def test_generate_and_cache_audio_api_error(self, mock_get_cache_file, mock_openai_class):
        """Test function handles API errors properly."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_file = Path(temp_dir) / "error.mp3"
            mock_get_cache_file.return_value = cache_file
            
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client
            
            # Create proper async context manager that raises exception
            @asynccontextmanager
            async def mock_context_manager(*args, **kwargs):
                raise Exception("API Error")
                yield  # This won't be reached
            
            mock_client.audio.speech.with_streaming_response.create = mock_context_manager
            
            config = {
                "api_key": "test-key",
                "model": "gpt-4o-mini-tts",
                "voice": "nova",
                "instructions": "test instructions",
                "response_format": "mp3"
            }
            
            # Execute & Verify
            with pytest.raises(Exception) as exc_info:
                await generate_and_cache_audio("test text", config)
            
            assert "API Error" in str(exc_info.value)
            assert not cache_file.exists()
    
    @patch('speaky.tts.AsyncOpenAI')
    @patch('speaky.tts.get_cache_file')
    @pytest.mark.asyncio
    async def test_generate_and_cache_audio_file_write_error(self, mock_get_cache_file, mock_openai_class):
        """Test function handles file write errors."""
        # Setup - use a path that can't be written to
        invalid_cache_file = Path("/invalid/path/file.mp3")
        mock_get_cache_file.return_value = invalid_cache_file
        
        mock_client = AsyncMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = AsyncMock()
        
        # Create async iterator for iter_bytes
        async def mock_async_iter():
            yield b'data'
        
        mock_response.iter_bytes = mock_async_iter
        
        # Create proper async context manager
        @asynccontextmanager
        async def mock_context_manager(*args, **kwargs):
            yield mock_response
        
        mock_client.audio.speech.with_streaming_response.create = mock_context_manager
        
        config = {
            "api_key": "test-key",
            "model": "gpt-4o-mini-tts",
            "voice": "nova",
            "instructions": "test instructions",
            "response_format": "mp3"
        }
        
        # Execute & Verify
        with pytest.raises(Exception):
            await generate_and_cache_audio("test text", config)
    
    @patch('speaky.tts.get_cache_file')
    @pytest.mark.asyncio
    async def test_generate_and_cache_audio_parameters(self, mock_get_cache_file):
        """Test function passes correct parameters to get_cache_file."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_file = Path(temp_dir) / "params.mp3"
            cache_file.touch()
            mock_get_cache_file.return_value = cache_file
            
            config = {
                "voice": "alloy",
                "instructions": "custom instructions"
            }
            
            # Execute
            await generate_and_cache_audio("custom text", config)
            
            # Verify parameters passed correctly
            mock_get_cache_file.assert_called_once_with(
                "custom text", "alloy", "custom instructions"
            )