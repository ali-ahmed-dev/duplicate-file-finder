# Duplicate File Finder

A Python CLI tool that scans folders recursively and detects duplicate files by comparing file size first, then SHA-256 hash to confirm exact matches.

Built with Python's standard library, with a focus on **reliability, memory efficiency, and safe file analysis**.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-14%20Passed-brightgreen)
![Version](https://img.shields.io/badge/Version-1.1.0-orange)

---

## 📌 Features

* Recursively scan a folder for all files.
* Group files by size to narrow down potential duplicates.
* Confirm duplicates using SHA-256 hashing.
* Skip empty files, symlinks, and common system directories (`.git`, `__pycache__`, `.venv`, `venv`, `env`, `node_modules`).
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
* Command-line interface (CLI) powered by `argparse`.
* Version flag (`--version`).
* Type hints and comprehensive docstrings.
* 14 unit tests covering all core functionality.
* Uses only Python's **standard library**.

---

## 🧠 How It Works

The tool uses a two-stage detection strategy to avoid unnecessary hashing:

```text
Input Folder
     │
     ▼
Scan Files (recursive)
     │
     ▼
Group by Size
     │
     ▼
For Groups > 1:
     │
     ▼
Calculate SHA-256
     │
     ▼
Group by Hash
     │
     ▼
Generate Report
```

**Why two stages?** Files with different sizes can never be duplicates. By grouping by size first, we only hash files that could actually be duplicates — saving significant processing time.

---

## ▶️ Usage

### 1. Clone the repository

    git clone https://github.com/ali-ahmed-dev/duplicate-file-finder.git

### 2. Enter the project directory

    cd duplicate-file-finder

### 3. Run the tool

    python duplicate_file_finder.py /path/to/folder

**Windows example:**

    python duplicate_file_finder.py "C:\Users\Username\Documents"

**Git Bash example:**

    python duplicate_file_finder.py /c/Users/Username/Documents

---

## Command-Line Options

| Option | Description |
| :--- | :--- |
| `folder` | (Required) Path to the folder to scan. |
| `--version` | Display the current version and exit. |
| `-h`, `--help` | Display the help message and exit. |

---

## Examples

### Scan a folder

    python duplicate_file_finder.py /path/to/folder

### Scan the current directory

    python duplicate_file_finder.py .

### Display help

    python duplicate_file_finder.py --help

### Display version

    python duplicate_file_finder.py --version

---

## Example Output

    ==================================================
                     DUPLICATE FILE FINDER
    ==================================================
    Scan Date: 2026-09-16 02:32:52
    Total files scanned: 10
    Total size: 334905027 bytes
    Potential duplicate groups by size: 2

    --- Duplicate Files by Hash ---
    Hash: 398882beb89df4eb05ee3f804090d6a583c39778ff4983336570905f924d3113
         /path/to/battery-report.html
         /path/to/copy-of-battery-report.html

    --------------------------------------------------
                     SUMMARY REPORT
    --------------------------------------------------
    Duplicate groups: 2
    Duplicate files (extra copies): 2
    Wasted space: 160630492 bytes
    Percentage duplicated: 20.00%
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

**Current Version: 1.1.0**

This version includes:

* Recursive folder scanning.
* Size-based grouping.
* SHA-256 duplicate confirmation.
* Command-line interface with `argparse`.
* Version flag.
* Detailed report with summary, wasted space, and percentages.
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

    Day 12 (Aug 24):
    feat: add CLI support with argparse and version flag

This development history is intentionally preserved to show the actual evolution of the project.

---

## 🚀 Future Improvements

Potential future enhancements include:

* Export reports to JSON or CSV
* Add option to safely delete duplicates (with confirmation and dry-run)
* Add progress indicator for large folders
* Support excluding user-defined directories via CLI
* Colorized terminal output

---

## ⚠️ Disclaimer

This tool **only detects** duplicate files. It does **not** delete, move, or modify any files.

Always review the report carefully before taking manual action.

---

## 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

## Author

**Ali Ahmed**

GitHub: https://github.com/ali-ahmed-dev

---

**Part of the File Management Tools collection.**