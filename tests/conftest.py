"""
Shared pytest fixtures for Duplicate File Finder tests.

This file allows running existing unittest-based tests via pytest
without modifying the original test file.

Note: The project uses Python's built-in unittest framework.
      pytest is used only as a convenient test runner.
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """
    Provide a temporary directory that is automatically cleaned up.
    
    Yields:
        Path: Path to the temporary directory.
    """
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def temp_dir_with_duplicates(temp_dir):
    """
    Create a temporary directory with duplicate and unique files.
    
    Yields:
        Path: Path to the temporary directory with test files.
    """
    # Duplicate pair
    (temp_dir / "file1.txt").write_text("duplicate content", encoding="utf-8")
    (temp_dir / "file2.txt").write_text("duplicate content", encoding="utf-8")
    
    # Unique files
    (temp_dir / "unique1.txt").write_text("unique content A", encoding="utf-8")
    (temp_dir / "unique2.txt").write_text("unique content B", encoding="utf-8")
    
    yield temp_dir