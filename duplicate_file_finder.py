"""
Duplicate File Finder

A simple tool that scans a folder recursively and detects duplicate files
by comparing file size first, then SHA-256 hash to confirm exact matches.

This is an educational project built with Python's standard library only.
"""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import json




# ===================== CONSTANTS =====================
CHUNK_SIZE = 4096

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
}

HEADER = (
    "=" * 50
    + "\n                 DUPLICATE FILE FINDER\n"
    + "=" * 50
)

FOOTER = (
    "=" * 50
    + "\n                 END OF REPORT\n"
    + "=" * 50
)

SUMMARY_HEADER = (
    "-" * 50
    + "\n                 SUMMARY REPORT\n"
    + "-" * 50
)


# ===================== FILE DISCOVERY =====================
def scan_folder(folder_path: Path) -> list[Path]:
    """
    Recursively scan a folder and return all valid files.

    Skips ignored directories, symlinks, and unreadable files.

    Args:
        folder_path (Path): The folder path to scan.

    Returns:
        list[Path]: A list of valid file paths.
    """
    files = []

    for file in folder_path.rglob("*"):
        if any(part in IGNORE_DIRS for part in file.parts):
            continue

        try:
            if file.is_file() and not file.is_symlink():
                files.append(file)
        except OSError:
            continue

    return files


# ===================== SIZE GROUPING =====================
def get_file_size(files: list[Path]) -> dict[int, list[Path]]:
    """
    Group files by their size in bytes.

    Empty files are skipped because they are not included
    in duplicate detection.

    Args:
        files (list[Path]): The list of files to group.

    Returns:
        dict[int, list[Path]]: A mapping of file size to files
        with that size.
    """
    files_by_size = {}

    for file in files:
        try:
            size = file.stat().st_size
        except OSError:
            continue

        if size == 0:
            continue

        files_by_size.setdefault(size, []).append(file)

    return files_by_size


# ===================== HASH CALCULATION =====================
def calculate_file_hash(file: Path) -> str | None:
    """
    Calculate the SHA-256 hash of a file.

    Args:
        file (Path): The file to hash.

    Returns:
        str | None: The hexadecimal hash, or None if the file
        cannot be read.
    """
    try:
        hash_obj = hashlib.sha256()

        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                hash_obj.update(chunk)

        return hash_obj.hexdigest()

    except OSError:
        return None


def get_file_hash(
    files_by_size: dict[int, list[Path]],
) -> dict[str, list[Path]]:
    """
    Calculate SHA-256 hashes for files with matching sizes.

    Only files that share the same size are hashed because files
    with different sizes cannot be exact duplicates.

    Args:
        files_by_size (dict[int, list[Path]]): Files grouped by size.

    Returns:
        dict[str, list[Path]]: A mapping of file hash to files
        with that hash.
    """
    files_by_hash = {}

    for files in files_by_size.values():
        if len(files) <= 1:
            continue

        for file in files:
            file_hash = calculate_file_hash(file)

            if file_hash is None:
                continue

            files_by_hash.setdefault(file_hash, []).append(file)

    return files_by_hash


# ===================== REPORT DATA =====================
def calculate_total_size(files: list[Path]) -> int:
    """
    Calculate the total size of all files in bytes.

    Args:
        files (list[Path]): The list of files.

    Returns:
        int: Total size in bytes.
    """
    total = 0

    for file in files:
        try:
            total += file.stat().st_size
        except OSError:
            continue

    return total


def build_report_data(
    folder: Path,
    files: list[Path],
    files_by_size: dict[int, list[Path]],
    files_by_hash: dict[str, list[Path]],
    scan_date: str,
) -> dict:
    """
    Build a structured dictionary with all report information.

    Args:
        folder (Path): The scanned folder.
        files (list[Path]): All scanned files.
        files_by_size (dict[int, list[Path]]): Files grouped by size.
        files_by_hash (dict[str, list[Path]]): Files grouped by hash.
        scan_date (str): Timestamp of the scan.

    Returns:
        dict: Structured report data.
    """
    total_size = calculate_total_size(files)

    potential_duplicates = sum(
        1 for group in files_by_size.values() if len(group) > 1
    )

    duplicate_groups = []

    for file_hash, duplicate_files in files_by_hash.items():
        if len(duplicate_files) <= 1:
            continue

        try:
            file_size = duplicate_files[0].stat().st_size
        except OSError:
            file_size = 0

        duplicate_groups.append(
            {
                "hash": file_hash,
                "size_bytes": file_size,
                "files": [str(file) for file in duplicate_files],
            }
        )

    duplicate_group_count = len(duplicate_groups)

    duplicate_file_count = sum(
        len(group["files"]) - 1
        for group in duplicate_groups
    )

    wasted_size = sum(
        group["size_bytes"] * (len(group["files"]) - 1)
        for group in duplicate_groups
    )

    percentage = (
        duplicate_file_count / len(files) * 100
        if files
        else 0
    )

    return {
        "scan_date": scan_date,
        "folder": str(folder),
        "total_files": len(files),
        "total_size_bytes": total_size,
        "potential_duplicate_groups": potential_duplicates,
        "duplicate_groups": duplicate_group_count,
        "duplicate_files": duplicate_file_count,
        "wasted_space_bytes": wasted_size,
        "percentage_duplicated": round(percentage, 2),
        "groups": duplicate_groups,
    }


# ===================== REPORT OUTPUT =====================
def print_terminal_report(data: dict) -> None:
    """
    Print the human-readable report to the terminal.

    Args:
        data (dict): Structured report data.
    """
    print(HEADER)
    print("Scan Date:", data["scan_date"])
    print("Total files scanned:", data["total_files"])
    print("Total size:", data["total_size_bytes"], "bytes")
    print(
        "Potential duplicate groups by size:",
        data["potential_duplicate_groups"],
    )

    print("\n--- Duplicate Files by Hash ---")

    if not data["groups"]:
        print("No duplicate files found.")
    else:
        for group in data["groups"]:
            print("Hash:", group["hash"])

            for file in group["files"]:
                print("    ", file)

    print(SUMMARY_HEADER)
    print("Duplicate groups:", data["duplicate_groups"])
    print("Duplicate files (extra copies):", data["duplicate_files"])
    print("Wasted space:", data["wasted_space_bytes"], "bytes")
    print(
        "Percentage duplicated:",
        f"{data['percentage_duplicated']:.2f}%",
    )
    print(FOOTER)


def export_to_json(
    data: dict,
    output_dir: Path,
    timestamp: datetime,
) -> bool:
    """
    Export the report data to a JSON file.

    Args:
        data (dict): Structured report data.
        output_dir (Path): Directory to save the JSON report.
        timestamp (datetime): Timestamp used for the report filename.

    Returns:
        bool: True if the report was exported successfully,
        otherwise False.
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as error:
        print(
            f"Error: Could not create output directory "
            f"{output_dir}. {error}"
        )
        return False

    filename = (
        f"duplicate_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    )
    report_path = output_dir / filename

    try:
        report_path.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )
    except (PermissionError, OSError) as error:
        print(
            f"Error: Could not write JSON report "
            f"to {report_path}. {error}"
        )
        return False

    print(f"JSON report exported to {report_path}")
    return True


# ===================== ARGUMENT PARSER =====================
def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the CLI argument parser.

    Returns:
        argparse.ArgumentParser: The configured parser.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Scan a folder recursively and detect duplicate files "
            "by comparing file size first, then SHA-256 hash."
        ),
        epilog="""
Examples:
  %(prog)s /path/to/folder
  %(prog)s "C:\\Users\\Username\\Documents"
  %(prog)s . --json
  %(prog)s /path/to/folder --json --output ./reports
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "folder",
        help="Path to the folder to scan",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Export the report as a JSON file",
    )

    parser.add_argument(
        "-o",
        "--output",
        help=(
            "Directory to save the JSON report "
            "(requires --json)"
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Duplicate File Finder v1.2.2",
    )

    return parser


# ===================== MAIN =====================
def main() -> int:
    """
    Run the duplicate file finder as a CLI tool.

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.output and not args.json:
        parser.error("--output requires --json")

    folder = Path(args.folder)

    if not folder.exists():
        print(f"Error: The provided path does not exist: {folder}")
        return 1

    if not folder.is_dir():
        print(f"Error: The provided path is not a valid directory: {folder}")
        return 1

    print(f"Scanning: {folder}\n")

    files = scan_folder(folder)

    if not files:
        print(HEADER)
        print("No files found in the specified folder.")
        print(FOOTER)
        return 0

    files_by_size = get_file_size(files)
    files_by_hash = get_file_hash(files_by_size)

    scan_timestamp = datetime.now()
    scan_date = scan_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    data = build_report_data(
        folder,
        files,
        files_by_size,
        files_by_hash,
        scan_date,
    )

    print_terminal_report(data)

    if args.json:
        output_dir = (
            Path(args.output)
            if args.output
            else Path.cwd()
        )

        if not export_to_json(
            data,
            output_dir,
            scan_timestamp,
        ):
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())