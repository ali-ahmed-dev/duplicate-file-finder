# Duplicate File Finder

A Python tool that scans folders recursively and detects duplicate files by comparing file size first, then SHA-256 hash to confirm exact matches.

This project was created as an **educational project** to practice file system traversal, hashing, and report generation.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-14%20Passed-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.1-orange)
![Educational](https://img.shields.io/badge/Project-Educational-purple)

---

## 📌 Features

* Recursively scan a folder for all files.
* Group files by size to narrow down potential duplicates.
* Confirm duplicates using SHA-256 hashing.
* Skip empty files, symlinks, and common system directories (`.git`, `__pycache__`, etc.).
* Detailed report including:
  * Total files scanned.
  * Total size in bytes.
  * Potential duplicate groups by size.
  * Confirmed duplicate files by hash.
  * Duplicate groups count.
  * Extra copies count.
  * Wasted disk space.
  * Percentage duplicated.
* Graceful handling of edge cases (empty folders, permission errors, invalid paths).
* Type hints and comprehensive docstrings.
* 14 unit tests covering all core functionality.
* Uses only Python's **standard library**.

---

## 🧠 Educational Purpose

The main purpose of this project is to practice and demonstrate several Python concepts in a small, complete application.

### Concepts practiced

* Recursive folder traversal with `pathlib`
* File metadata (size) inspection
* SHA-256 hashing with `hashlib`
* Chunk-based file reading for memory efficiency
* Dictionary grouping with `setdefault`
* Exception handling (`OSError`)
* Symlink and system directory filtering
* Report generation
* Unit testing with `unittest`
* Type hints and docstrings
* Git and GitHub workflow

The project also demonstrates how a simple application can evolve through multiple development stages instead of being written as one large final version.

---

## ▶️ Usage

### 1. Clone the repository

    git clone https://github.com/ali-ahmed-dev/duplicate-file-finder.git

### 2. Enter the project directory

    cd duplicate-file-finder

### 3. Run the application

    python duplicate_file_finder.py

Then enter the folder path when prompted.

Example output:

    ==================================================
                     DUPLICATE FILE FINDER
    ==================================================
    Scan Date: 2026-08-17 14:23:18
    Total files scanned: 42
    Total size: 15234567 bytes
    Potential duplicate groups by size: 3

    --- Duplicate Files by Hash ---
    Hash: a3f5b2c8...
        /path/to/photo1.jpg
        /path/to/photo1_copy.jpg

    --------------------------------------------------
                     SUMMARY REPORT
    --------------------------------------------------
    Duplicate groups: 2
    Duplicate files (extra copies): 3
    Wasted space: 2456789 bytes
    Percentage duplicated: 7.14%
    ==================================================
                     END OF REPORT
    ==================================================

---

## 🧪 Tests

The project includes **14 automated unit tests** using Python's built-in `unittest` framework.

The tests cover:

* Scanning empty and non-empty folders
* Recursive scanning
* Ignoring system directories (`.git`, `__pycache__`)
* Grouping files by size
* Skipping empty files
* SHA-256 hash calculation (known content, same content, different content)
* Duplicate detection by hash
* Same-size different-content handling
* Ignoring single-file groups
* Total size calculation

Run the tests with:

    python -m unittest discover -s tests -t . -v

Current result:

    Ran 14 tests in 0.147s

    OK

---

## 📁 Project Structure

    duplicate-file-finder/
    │
    ├── duplicate_file_finder.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_duplicate_file_finder.py
    ├── .gitignore
    ├── LICENSE
    └── README.md

---

## 🛠️ Requirements

* Python 3.x
* No external Python packages are required.

The application uses only Python's standard library.

---

## 📜 Version

**Current Version: 1.0.1**

This version includes:

* Recursive folder scanning.
* Size-based grouping.
* SHA-256 duplicate confirmation.
* Detailed report with summary and percentages.
* Edge case handling (empty folders, permission errors, invalid paths).
* Skips empty files, symlinks, and common system directories.
* 14 unit tests covering all core functionality.
* Type hints and docstrings.

---

## 📈 Development History

The project was developed incrementally through separate Git commits over several days:

    Day 1 (Aug 12):
    Initial commit: scan folder and list all files
            ↓
    feat: group files by size to detect potential duplicates
            ↓
    feat: add SHA-256 hashing to confirm duplicate files

    Day 2 (Aug 13):
    feat: add report header, footer, and generate_report function
            ↓
    feat: add scan statistics (file count, total size, duplicate groups)
            ↓
    feat: add summary section with duplicate groups, files, and percentage
            ↓
    fix: handle edge cases (empty folder, permission errors, invalid path)
            ↓
    refactor: extract hash logic into separate function and add CHUNK_SIZE constant
            ↓
    style: final polish with section headers and improved messages

    Day 3 (Aug 14):
    docs: add README and MIT license

    Day 5 (Aug 17):
    fix: skip empty files, symlinks, and ignore system directories; improve duplicate count accuracy
            ↓
    test: add 14 unit tests covering core functionality

This development history is intentionally preserved to show the actual evolution of the project.

---

## 🚀 Future Improvements

Potential future enhancements include:

* Add CLI arguments using `argparse`
* Export reports to JSON or CSV
* Add colorized terminal output
* Add option to safely delete duplicates (with confirmation and dry-run)
* Add progress indicator for large folders
* Support for excluding user-defined directories via CLI

---

## ⚠️ Disclaimer

This tool **only detects** duplicate files. It does **not** delete, move, or modify any files.

Always review the report carefully before taking manual action.

---

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

**Built as part of my Python learning journey.**