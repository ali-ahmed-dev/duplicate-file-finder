"""
Duplicate File Finder - Scan a folder and detect duplicates by size and hash.
"""

import hashlib
from pathlib import Path


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
        if file.is_file():
            files.append(file)
    return files


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
        size = file.stat().st_size
        if size in files_by_size:
            files_by_size[size].append(file)
        else:
            files_by_size[size] = [file]
    return files_by_size


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
        if len(files) > 1:
            for file in files:
                hash_obj = hashlib.sha256()
                with open(file, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_obj.update(chunk)
                file_hash = hash_obj.hexdigest()
                if file_hash in files_by_hash:
                    files_by_hash[file_hash].append(file)
                else:
                    files_by_hash[file_hash] = [file]
    return files_by_hash


def main() -> None:
    """Run the duplicate file finder."""
    path_input = input("Enter the folder path:\n").strip()
    folder = Path(path_input)

    if not folder.is_dir():
        print("Error: The provided path is not a valid directory.")
        return

    files = scan_folder(folder)
    files_by_size = get_file_size(files)
    files_by_hash = get_file_hash(files_by_size)

    print(f"Total files found: {len(files)}")
    print(f"Unique file sizes: {len(files_by_size)}")

    potential_duplicates = sum(
        1 for group in files_by_size.values() if len(group) > 1
    )
    print(f"Potential duplicate groups by size: {potential_duplicates}")

    print("\n--- Duplicate Files by Hash ---")
    for file_hash, dup_files in files_by_hash.items():
        if len(dup_files) > 1:
            print(f"Hash: {file_hash}")
            for f in dup_files:
                print(f"    {f}")


if __name__ == "__main__":
    main()