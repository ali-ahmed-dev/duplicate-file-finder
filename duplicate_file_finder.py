"""
Duplicate File Finder

A simple tool that scans a folder recursively and detects duplicate files
by comparing file size first, then SHA-256 hash to confirm exact matches.

This is an educational project built with Python's standard library only.
"""

import hashlib
import datetime
from pathlib import Path


# ===================== CONSTANTS =====================
CHUNK_SIZE = 4096
HEADER = "=" * 50 + "\n                 DUPLICATE FILE FINDER\n" + "=" * 50
FOOTER = "=" * 50 + "\n                 END OF REPORT\n" + "=" * 50
SUMMARY_HEADER = "-" * 50 + "\n                 SUMMARY REPORT\n" + "-" * 50


# ===================== FILE DISCOVERY =====================
def scan_folder(folder_path: Path) -> list[Path]:
    """
    Recursively scan a folder and return all files.

    Args:
        folder_path (Path): The folder path to scan.

    Returns:
        list[Path]: A list of all file paths.
    """
    files = []
    for file in folder_path.rglob("*"):
        try:
            if file.is_file():
                files.append(file)
        except OSError:
            continue
    return files


# ===================== SIZE GROUPING =====================
def get_file_size(files: list[Path]) -> dict[int, list[Path]]:
    """
    Group files by their size in bytes.

    Args:
        files (list[Path]): The list of files to group.

    Returns:
        dict[int, list[Path]]: A mapping of file size to files with that size.
    """
    files_by_size = {}
    for file in files:
        try:
            size = file.stat().st_size
        except OSError:
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
        str | None: The hexadecimal hash, or None if the file cannot be read.
    """
    try:
        hash_obj = hashlib.sha256()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except OSError:
        return None


def get_file_hash(files_by_size: dict[int, list[Path]]) -> dict[str, list[Path]]:
    """
    Calculate SHA-256 hashes for files with matching sizes to confirm duplicates.

    Args:
        files_by_size (dict[int, list[Path]]): Files grouped by size.

    Returns:
        dict[str, list[Path]]: A mapping of file hash to files with that hash.
    """
    files_by_hash = {}
    for size, files in files_by_size.items():
        if len(files) <= 1:
            continue
        for file in files:
            file_hash = calculate_file_hash(file)
            if file_hash is None:
                continue
            files_by_hash.setdefault(file_hash, []).append(file)
    return files_by_hash


# ===================== REPORT GENERATION =====================
def generate_report(
    files: list[Path],
    files_by_size: dict[int, list[Path]],
    files_by_hash: dict[str, list[Path]]
) -> None:
    """
    Generate and print the duplicate file report.

    Args:
        files (list[Path]): All scanned files.
        files_by_size (dict[int, list[Path]]): Files grouped by size.
        files_by_hash (dict[str, list[Path]]): Files grouped by hash.
    """
    print(HEADER)
    print("Scan Date:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Total files scanned:", len(files))

    total_size = sum(file.stat().st_size for file in files)
    print("Total size:", total_size, "bytes")

    potential_duplicates = sum(
        1 for group in files_by_size.values() if len(group) > 1
    )
    print("Potential duplicate groups by size:", potential_duplicates)

    print("\n--- Duplicate Files by Hash ---")
    has_duplicates = False
    for file_hash, dup_files in files_by_hash.items():
        if len(dup_files) > 1:
            has_duplicates = True
            print("Hash:", file_hash)
            for f in dup_files:
                print("    ", f)

    if not has_duplicates:
        print("No duplicate files found.")

    print(SUMMARY_HEADER)
    duplicate_groups = sum(
        1 for group in files_by_hash.values() if len(group) > 1
    )
    duplicate_files = sum(
        len(group) for group in files_by_hash.values() if len(group) > 1
    )
    percentage = (duplicate_files / len(files) * 100) if files else 0

    print("Duplicate groups:", duplicate_groups)
    print("Duplicate files:", duplicate_files)
    print("Percentage duplicated:", f"{percentage:.2f}%")
    print(FOOTER)


# ===================== MAIN =====================
def main() -> None:
    """Run the duplicate file finder."""
    print("Welcome to the Duplicate File Finder!")

    path_input = input("Enter the folder path:\n").strip()

    if not path_input:
        print("Error: No path provided.")
        return

    folder = Path(path_input)

    if not folder.exists():
        print("Error: The provided path does not exist.")
        return

    if not folder.is_dir():
        print("Error: The provided path is not a valid directory.")
        return

    print(f"\nScanning: {folder}\n")

    files = scan_folder(folder)

    if not files:
        print(HEADER)
        print("No files found in the specified folder.")
        print(FOOTER)
        return

    files_by_size = get_file_size(files)
    files_by_hash = get_file_hash(files_by_size)
    generate_report(files, files_by_size, files_by_hash)


if __name__ == "__main__":
    main()