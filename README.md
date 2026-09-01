```markdown
# Duplicate File Finder

A Python CLI tool that scans folders recursively and detects duplicate files by comparing file size first, then SHA-256 hash to confirm exact matches.

Built with Python's standard library, with a focus on **reliability, memory efficiency, and safe file analysis**.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-20%20Passed-brightgreen)
![CI](https://github.com/ali-ahmed-dev/duplicate-file-finder/actions/workflows/test.yml/badge.svg)
![Version](https://img.shields.io/badge/Version-1.2.2-orange)

---

## 📌 Features

* Recursively scan a folder for all files.
* Group files by size to narrow down potential duplicates.
* Confirm duplicates using SHA-256 hashing.
* Skip empty files, symlinks, and common system directories (`.git`, `__pycache__`, `.venv`, `venv`, `env`, `node_modules`).
* Detailed terminal report including:
  * Total files scanned.
  * Total size in bytes.
  * Potential duplicate groups by size.
  * Confirmed duplicate files by hash.
  * Duplicate groups count.
  * Extra copies count.
  * Wasted disk space.
  * Percentage duplicated.
* **JSON report export** (`--json`) for automation and integration.
* **Custom output directory** (`--output`) for generated JSON reports.
* Graceful handling of edge cases (empty folders, permission errors, invalid paths).
* Command-line interface (CLI) powered by `argparse`.
* Version flag (`--version`).
* Type hints and comprehensive docstrings.
* 20 unit tests covering all core functionality.
* **Automated testing** via GitHub Actions (Python 3.8 → 3.13).
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
     │
     ├── Terminal
     └── JSON (optional)
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
| `--json` | Export the report as a JSON file. |
| `-o`, `--output` | Directory to save the JSON report (default: current directory; requires `--json`). |
| `--version` | Display the current version and exit. |
| `-h`, `--help` | Display the help message and exit. |

---

## Examples

### Scan a folder

    python duplicate_file_finder.py /path/to/folder

### Scan the current directory

    python duplicate_file_finder.py .

### Scan and export a JSON report

    python duplicate_file_finder.py /path/to/folder --json

### Scan and save the JSON report to a custom directory

    python duplicate_file_finder.py /path/to/folder --json --output ./reports

### Display help

    python duplicate_file_finder.py --help

### Display version

    python duplicate_file_finder.py --version

---

## Example Output

### Terminal Report

```
==================================================
                 DUPLICATE FILE FINDER
==================================================
Scan Date: 2026-08-28 21:30:15
Total files scanned: 10
Total size: 334905027 bytes
Potential duplicate groups by size: 1

--- Duplicate Files by Hash ---
Hash: 398882beb89df4eb05ee3f804090d6a583c39778ff4983336570905f924d3113
     /path/to/battery-report.html
     /path/to/copy-of-battery-report.html

--------------------------------------------------
                 SUMMARY REPORT
--------------------------------------------------
Duplicate groups: 1
Duplicate files (extra copies): 1
Wasted space: 80315246 bytes
Percentage duplicated: 10.00%
==================================================
                 END OF REPORT
==================================================
```

### JSON Report

When `--json` is used, a timestamped JSON file is generated with the following structure:

```json
{
    "scan_date": "2026-08-28 21:30:15",
    "folder": "/path/to/folder",
    "total_files": 10,
    "total_size_bytes": 334905027,
    "potential_duplicate_groups": 1,
    "duplicate_groups": 1,
    "duplicate_files": 1,
    "wasted_space_bytes": 80315246,
    "percentage_duplicated": 10.0,
    "groups": [
        {
            "hash": "398882beb89df4eb05ee3f804090d6a583c39778ff4983336570905f924d3113",
            "size_bytes": 80315246,
            "files": [
                "/path/to/battery-report.html",
                "/path/to/copy-of-battery-report.html"
            ]
        }
    ]
}
```

Reports are saved with timestamped filenames:

```text
duplicate_report_20260828_213015.json
```

---

## 🧪 Tests

The project includes **20 automated unit tests** using Python's built-in `unittest` framework.

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
* Report data construction (structure, no duplicates, wasted space)
* JSON export (file creation, valid content, filename format)

Run the tests with:

    python -m unittest discover -s tests -t . -v

Current result:

    Ran 20 tests in 0.167s

    OK

---

## ⚙️ Continuous Integration

Tests are automatically run on every push and pull request to `main` via **GitHub Actions**.

The workflow tests the project against **six Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13.

The workflow file is located at:

    .github/workflows/test.yml

---

## 📁 Project Structure

    duplicate-file-finder/
    │
    ├── .github/
    │   └── workflows/
    │       └── test.yml
    ├── duplicate_file_finder.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_duplicate_file_finder.py
    ├── .gitignore
    ├── LICENSE
    └── README.md

JSON reports are generated at runtime and are not tracked in the repository (see `.gitignore`).

---

## 🛠️ Requirements

* Python 3.x
* No external Python packages are required.

The application uses only Python's standard library.

---

## 📜 Version

**Current Version: 1.2.2**

This version includes:

* Recursive folder scanning.
* Size-based grouping.
* SHA-256 duplicate confirmation.
* Command-line interface with `argparse`.
* Version flag.
* JSON report export (`--json`).
* Configurable output directory (`--output`).
* Detailed terminal report with summary, wasted space, and percentages.
* Edge case handling (empty folders, permission errors, invalid paths).
* Skips empty files, symlinks, and common system directories.
* 20 unit tests covering all core functionality.
* Type hints and docstrings.
* Automated CI/CD via GitHub Actions (Python 3.8 → 3.13).

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

    Day 14 (Aug 26):
    docs: add project roadmap and guiding principles

    Day 15 (Aug 27):
    feat: add JSON report output and custom output directory

    Day 16 (Aug 28):
    test: expand test suite to 20 tests covering report and JSON export

    Day 20 (Sep 1):
    ci: add GitHub Actions workflow for automated testing
            ↓
    fix: add __future__ annotations for Python 3.8 compatibility

This development history is intentionally preserved to show the actual evolution of the project.

---

## 🚀 Future Improvements

Potential future enhancements include:

* Export reports to CSV format
* Add progress indicator for large folders
* Support excluding user-defined directories via CLI
* Support filtering by extension and minimum size
* Parallel hashing for large directories
* Safe quarantine and deletion (with dry-run and manifest)

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