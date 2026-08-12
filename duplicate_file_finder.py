"""
Duplicate File Finder - Scan a folder and list all files.
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


def main() -> None:
    """Run the duplicate file finder."""
    path_input = input("Enter the folder path:\n").strip()
    folder = Path(path_input)

    if not folder.is_dir():
        print("Error: The provided path is not a valid directory.")
        return

    files = scan_folder(folder)

    print(f"Total files found: {len(files)}")
    for file in files:
        print(file)


if __name__ == "__main__":
    main()