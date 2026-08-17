"""
Unit tests for the Duplicate File Finder.
"""

import tempfile
import unittest
from pathlib import Path

import duplicate_file_finder


class TestScanFolder(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scan_empty_folder(self):
        files = duplicate_file_finder.scan_folder(self.root)
        self.assertEqual(files, [])

    def test_scan_returns_all_files(self):
        (self.root / "a.txt").write_text("a", encoding="utf-8")
        (self.root / "b.txt").write_text("b", encoding="utf-8")
        (self.root / "c.txt").write_text("c", encoding="utf-8")

        files = duplicate_file_finder.scan_folder(self.root)
        self.assertEqual(len(files), 3)

    def test_scan_recursive(self):
        sub = self.root / "sub"
        sub.mkdir()
        (self.root / "a.txt").write_text("a", encoding="utf-8")
        (sub / "b.txt").write_text("b", encoding="utf-8")

        files = duplicate_file_finder.scan_folder(self.root)
        self.assertEqual(len(files), 2)

    def test_scan_ignores_system_directories(self):
        (self.root / "a.txt").write_text("a", encoding="utf-8")

        git_dir = self.root / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("data", encoding="utf-8")

        pycache = self.root / "__pycache__"
        pycache.mkdir()
        (pycache / "cache.pyc").write_text("data", encoding="utf-8")

        files = duplicate_file_finder.scan_folder(self.root)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "a.txt")


class TestGetFileSize(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_groups_by_size(self):
        f1 = self.root / "a.txt"
        f2 = self.root / "b.txt"
        f3 = self.root / "c.txt"

        f1.write_text("aaa", encoding="utf-8")
        f2.write_text("bbb", encoding="utf-8")
        f3.write_text("cc", encoding="utf-8")

        files_by_size = duplicate_file_finder.get_file_size([f1, f2, f3])

        self.assertEqual(len(files_by_size), 2)
        self.assertEqual(len(files_by_size[3]), 2)
        self.assertEqual(len(files_by_size[2]), 1)

    def test_skips_empty_files(self):
        f1 = self.root / "empty1.txt"
        f2 = self.root / "empty2.txt"
        f3 = self.root / "nonempty.txt"

        f1.write_text("", encoding="utf-8")
        f2.write_text("", encoding="utf-8")
        f3.write_text("data", encoding="utf-8")

        files_by_size = duplicate_file_finder.get_file_size([f1, f2, f3])

        self.assertNotIn(0, files_by_size)
        self.assertEqual(len(files_by_size), 1)


class TestCalculateFileHash(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_hash_of_known_content(self):
        file = self.root / "test.txt"
        file.write_text("hello", encoding="utf-8")

        result = duplicate_file_finder.calculate_file_hash(file)

        expected = (
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        )
        self.assertEqual(result, expected)

    def test_same_content_same_hash(self):
        f1 = self.root / "a.txt"
        f2 = self.root / "b.txt"
        f1.write_text("same content", encoding="utf-8")
        f2.write_text("same content", encoding="utf-8")

        self.assertEqual(
            duplicate_file_finder.calculate_file_hash(f1),
            duplicate_file_finder.calculate_file_hash(f2)
        )

    def test_different_content_different_hash(self):
        f1 = self.root / "a.txt"
        f2 = self.root / "b.txt"
        f1.write_text("content A", encoding="utf-8")
        f2.write_text("content B", encoding="utf-8")

        self.assertNotEqual(
            duplicate_file_finder.calculate_file_hash(f1),
            duplicate_file_finder.calculate_file_hash(f2)
        )


class TestGetFileHash(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_detects_duplicates(self):
        f1 = self.root / "a.txt"
        f2 = self.root / "b.txt"
        f3 = self.root / "c.txt"

        f1.write_text("duplicate", encoding="utf-8")
        f2.write_text("duplicate", encoding="utf-8")
        f3.write_text("unique", encoding="utf-8")

        files_by_size = duplicate_file_finder.get_file_size([f1, f2, f3])
        files_by_hash = duplicate_file_finder.get_file_hash(files_by_size)

        duplicate_groups = [
            g for g in files_by_hash.values() if len(g) > 1
        ]
        self.assertEqual(len(duplicate_groups), 1)
        self.assertEqual(len(duplicate_groups[0]), 2)

    def test_same_size_different_content(self):
        f1 = self.root / "a.txt"
        f2 = self.root / "b.txt"

        f1.write_text("aaa", encoding="utf-8")
        f2.write_text("bbb", encoding="utf-8")

        files_by_size = duplicate_file_finder.get_file_size([f1, f2])
        files_by_hash = duplicate_file_finder.get_file_hash(files_by_size)

        duplicate_groups = [
            g for g in files_by_hash.values() if len(g) > 1
        ]
        self.assertEqual(len(duplicate_groups), 0)

    def test_ignores_single_file_groups(self):
        f1 = self.root / "a.txt"
        f1.write_text("unique", encoding="utf-8")

        files_by_size = duplicate_file_finder.get_file_size([f1])
        files_by_hash = duplicate_file_finder.get_file_hash(files_by_size)

        self.assertEqual(files_by_hash, {})


class TestCalculateTotalSize(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_total_size_of_files(self):
        f1 = self.root / "a.txt"
        f2 = self.root / "b.txt"
        f1.write_text("12345", encoding="utf-8")
        f2.write_text("123", encoding="utf-8")

        total = duplicate_file_finder.calculate_total_size([f1, f2])
        self.assertEqual(total, 8)

    def test_total_size_empty_list(self):
        total = duplicate_file_finder.calculate_total_size([])
        self.assertEqual(total, 0)


if __name__ == "__main__":
    unittest.main()