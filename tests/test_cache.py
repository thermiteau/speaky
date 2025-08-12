"""Tests for cache module."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from speaky.cache import generate_cache_key, get_cache_file, clear_cache


class TestGenerateCacheKey:
    """Tests for generate_cache_key function."""
    
    def test_generate_cache_key_consistent(self):
        """Test that same inputs generate same cache key."""
        # Setup
        text = "Hello world"
        voice = "nova"
        instructions = "Speak clearly"
        
        # Execute
        key1 = generate_cache_key(text, voice, instructions)
        key2 = generate_cache_key(text, voice, instructions)
        
        # Verify
        assert key1 == key2
        assert len(key1) == 32  # MD5 hash length
    
    def test_generate_cache_key_different_inputs(self):
        """Test that different inputs generate different cache keys."""
        # Execute
        key1 = generate_cache_key("text1", "nova", "instructions")
        key2 = generate_cache_key("text2", "nova", "instructions")
        key3 = generate_cache_key("text1", "alloy", "instructions")
        key4 = generate_cache_key("text1", "nova", "different instructions")
        
        # Verify
        keys = [key1, key2, key3, key4]
        assert len(set(keys)) == 4  # All keys should be unique
    
    def test_generate_cache_key_format(self):
        """Test cache key generation format."""
        # Setup
        text = "test"
        voice = "nova"
        instructions = "speak"
        expected_string = f"{text}::{voice}::{instructions}"
        
        # Execute
        key = generate_cache_key(text, voice, instructions)
        
        # Verify - check it's a valid MD5 hash
        import hashlib
        expected_key = hashlib.md5(expected_string.encode()).hexdigest()
        assert key == expected_key


class TestGetCacheFile:
    """Tests for get_cache_file function."""
    
    @patch('speaky.cache.get_cache_dir')
    def test_get_cache_file_path(self, mock_get_cache_dir):
        """Test get_cache_file returns correct path."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            mock_get_cache_dir.return_value = cache_dir
            
            # Execute
            result = get_cache_file("test", "nova", "instructions")
            
            # Verify
            assert result.parent == cache_dir
            assert result.suffix == ".mp3"
            assert len(result.stem) == 32  # MD5 hash length
    
    @patch('speaky.cache.get_cache_dir')
    def test_get_cache_file_consistent(self, mock_get_cache_dir):
        """Test get_cache_file returns consistent paths for same inputs."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            mock_get_cache_dir.return_value = cache_dir
            
            # Execute
            path1 = get_cache_file("test", "nova", "instructions")
            path2 = get_cache_file("test", "nova", "instructions")
            
            # Verify
            assert path1 == path2


class TestClearCache:
    """Tests for clear_cache function."""
    
    @patch('speaky.cache.get_cache_dir')
    def test_clear_cache_removes_mp3_files(self, mock_get_cache_dir, capsys):
        """Test clear_cache removes all mp3 files."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            mock_get_cache_dir.return_value = cache_dir
            
            # Create test files
            mp3_file1 = cache_dir / "test1.mp3"
            mp3_file2 = cache_dir / "test2.mp3"
            other_file = cache_dir / "test.txt"
            
            mp3_file1.touch()
            mp3_file2.touch()
            other_file.touch()
            
            # Execute
            clear_cache()
            
            # Verify
            assert not mp3_file1.exists()
            assert not mp3_file2.exists()
            assert other_file.exists()  # Non-mp3 files should remain
            
            # Check output message
            captured = capsys.readouterr()
            assert "✅ Cleared cache directory:" in captured.out
            assert str(cache_dir) in captured.out
    
    @patch('speaky.cache.get_cache_dir')
    def test_clear_cache_empty_directory(self, mock_get_cache_dir, capsys):
        """Test clear_cache works with empty directory."""
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            mock_get_cache_dir.return_value = cache_dir
            
            # Execute
            clear_cache()
            
            # Verify - should not raise error
            captured = capsys.readouterr()
            assert "✅ Cleared cache directory:" in captured.out