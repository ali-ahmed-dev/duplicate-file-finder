# Duplicate File Finder

A simple Python tool that scans a folder recursively and detects duplicate files by comparing file size first, then SHA-256 hash.

This project was created as an **educational project** to practice file system traversal, hashing, and report generation.

---

## 📌 Features

* Recursively scan a folder for all files.
* Group files by size to narrow down potential duplicates.
* Confirm duplicates using SHA-256 hashing.
* Generate a detailed report with:
  * Total files scanned.
  * Total size in bytes.
  * Potential duplicate groups by size.
  * Confirmed duplicate files by hash.
  * Summary with duplicate count and percentage.
* Graceful handling of empty folders, invalid paths, and permission errors.
* Type hints and comprehensive docstrings.
* Uses only Python's **standard library**.

---

## 🧠 Educational Purpose

The main purpose of this project is to practice and demonstrate several Python concepts in a small, complete application.

### Concepts practiced

* Recursive folder traversal with `pathlib`
* File metadata (size) inspection
* SHA-256 hashing with `hashlib`
* Chunk-based file reading for memory efficiency
* Dictionary grouping
* Report generation
* Exception handling (OSError)
* Type hints and docstrings
* Git and GitHub workflow

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
    Scan Date: 2026-08-13 20:07:41
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
    Duplicate files: 5
    Percentage duplicated: 11.90%
    ==================================================
                     END OF REPORT
    ==================================================

---

## 📁 Project Structure

    duplicate-file-finder/
    │
    ├── duplicate_file_finder.py
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

**Current Version: 1.0.0**

This version includes:

* Recursive folder scanning.
* Size-based grouping.
* SHA-256 duplicate confirmation.
* Detailed report with summary and percentages.
* Edge case handling (empty folders, permission errors, invalid paths).
* Type hints and docstrings.

---

## 📈 Development History

The project was developed incrementally through separate Git commits over two days:

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

This development history is intentionally preserved to show the actual evolution of the project.

---

## 🚀 Future Improvements

Potential future enhancements include:

* Add unit tests
* Add CLI arguments using `argparse`
* Add option to delete duplicates safely
* Export reports to JSON or CSV
* Add progress indicator for large folders
* Skip hidden or system files

---

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

**Built as part of my Python learning journey.**