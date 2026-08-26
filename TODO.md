# TODO - Duplicate File Finder

This document outlines the planned improvements and future roadmap for **Duplicate File Finder**.

The current release (**v1.1.0**) is a read-only duplicate detection tool. It scans files, compares their sizes, calculates SHA-256 hashes when necessary, and reports detected duplicates without modifying files.

Future features should preserve the project's core principle:

> **Detection is automatic. File operations are explicit.**

---

## 🚨 High Priority

These improvements focus on useful output, diagnostics, and practical CLI functionality.

### Output

* [ ] Add JSON report output (`--json`) for automation and integration.
* [ ] Add CSV report output (`--csv`) for spreadsheet analysis.

### Diagnostics

* [ ] Track and report files that could not be accessed or hashed.
* [ ] Report skipped files and ignored directories more clearly.

### Filters

* [ ] Support excluding user-defined directories (`--exclude <pattern>`).
* [ ] Support filtering by file extension (`--extensions .pdf,.jpg`).
* [ ] Support minimum file size filtering (`--min-size <bytes>`).

---

## 🛠️ Medium Priority

These improvements focus on usability and reporting.

### CLI

* [ ] Add progress indication for large scans.
* [ ] Support scanning multiple folders in one run.
* [ ] Add a summary-only output mode.

### Reporting

* [ ] Add HTML report output.
* [ ] Improve duplicate group information and statistics.
* [ ] Improve human-readable file size formatting.

### Quality

* [ ] Expand unit test coverage as new features are added.
* [ ] Add CLI-specific tests for arguments and exit codes.

---

## 💡 Low Priority

Quality-of-life improvements that can be added if they provide real value.

* [ ] Add colorized terminal output.
* [ ] Add `--top N` to show the largest duplicate groups.
* [ ] Add optional output file support.
* [ ] Improve handling and reporting of unusual filesystem errors.

---

## 🔒 Long-Term Goals

These features involve modifying or managing files and should only be considered after the read-only functionality is mature.

### Safe Isolation

* [ ] Add `--quarantine <dir>` to move selected duplicates to a quarantine directory.
* [ ] Generate a manifest documenting every file operation.
* [ ] Add interactive selection of files to keep.
* [ ] Require explicit confirmation before file operations.
* [ ] Add `--dry-run` support for file operations.

### File Deletion

* [ ] Add controlled duplicate deletion.
* [ ] Require explicit confirmation before deletion.
* [ ] Support configurable keep strategies.
* [ ] Add deletion safety limits.
* [ ] Support protected file patterns.
* [ ] Provide full undo capability using manifest files.

---

## 🚀 Future Performance Goals

These optimizations should only be introduced when real-world testing shows they are useful.

* [ ] Parallel file hashing using `concurrent.futures`.
* [ ] Hash caching using SQLite.
* [ ] Optimize scanning and hashing for very large directory trees.

---

## 🌐 Experimental / Future Ideas

These features may be considered if the project grows beyond local filesystem scanning.

* [ ] Support network paths such as SMB and NFS.
* [ ] Add watch mode for monitoring directories.
* [ ] Provide notifications when new duplicate files are detected.

---

## Project Roadmap

| Version | Focus                                 | Status       |
| ------- | ------------------------------------- | ------------ |
| v1.0.0  | Initial duplicate detection           | ✅ Released   |
| v1.0.1  | Unit tests and stability improvements | ✅ Released   |
| v1.1.0  | CLI with `argparse`                   | ✅ Current    |
| v1.2.0  | Output, diagnostics, and filters      | 🎯 Next      |
| v1.3.0  | Reporting and usability improvements  | ⏳ Planned    |
| v2.0.0  | Safe file management                  | 🔮 Long-term |

---

## Guiding Principles

These principles apply to every feature added to the project:

1. **Detection is automatic; file operations are explicit.**
2. **The read-only scanner must never modify scanned files.**
3. **Every file operation must require explicit user intent.**
4. **Destructive operations must provide a dry-run mode first.**
5. **File operations must be recorded in a manifest.**
6. **Protected files and patterns must be respected.**
7. **Expected filesystem errors should be handled and reported where possible.**
8. **New features should solve a real problem rather than add complexity for its own sake.**

---

Contributions, suggestions, and feature requests are welcome as the project continues to evolve.
