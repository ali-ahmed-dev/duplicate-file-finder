"""
Duplicate File Finder - Scan a folder and group files by size.
"""

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


def main() -> None:
    """Run the duplicate file finder."""
    path_input = input("Enter the folder path:\n").strip()
    folder = Path(path_input)

    if not folder.is_dir():
        print("Error: The provided path is not a valid directory.")
        return

    files = scan_folder(folder)
    files_by_size = get_file_size(files)

    print(f"Total files found: {len(files)}")
    print(f"Unique file sizes: {len(files_by_size)}")

    potential_duplicates = sum(
        1 for group in files_by_size.values() if len(group) > 1
    )
    print(f"Potential duplicate groups by size: {potential_duplicates}")


if __name__ == "__main__":
    main()