"""Sort files in a directory into subfolders by file type."""

import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf"},
    "audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"},
    "video": {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv"},
    "archives": {".zip", ".tar", ".gz", ".bz2", ".7z", ".rar", ".xz"},
    "code": {".py", ".js", ".ts", ".go", ".rs", ".java", ".c", ".cpp", ".sh"},
}


def classify(path):
    for folder, extensions in CATEGORIES.items():
        if path.suffix.lower() in extensions:
            return folder
    return None


def organize(directory, dry_run=False):
    moved = 0
    for item in sorted(directory.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        folder = classify(item)
        if folder is None:
            continue
        target = directory / folder
        target.mkdir(exist_ok=True)
        dest = target / item.name
        if dry_run:
            print(f"[dry-run] {item.name} -> {folder}/")
        else:
            shutil.move(str(item), str(dest))
        moved += 1
    return moved


def main():
    parser = argparse.ArgumentParser(description="organize files by extension")
    parser.add_argument("directory", nargs="?", default=".", help="directory to scan")
    parser.add_argument("--dry-run", action="store_true", help="print actions only")
    args = parser.parse_args()

    path = Path(args.directory)
    if not path.is_dir():
        print(f"error: {args.directory} is not a directory")
        return 1

    moved = organize(path, dry_run=args.dry_run)
    mode = "would move" if args.dry_run else "moved"
    print(f"{mode} {moved} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

