#!/usr/bin/env python3
"""Report the size of each subfolder, largest first.

Usage:
    python3 main.py <folder> [--top 10] [--human] [--include-files]
"""
import argparse
from pathlib import Path


def human_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{num_bytes} B"


def dir_size(path: Path) -> int:
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            try:
                total += p.stat().st_size
            except OSError:
                pass
    return total


def report(folder: Path, top: int, human: bool, include_files: bool):
    rows = []
    for child in sorted(folder.iterdir()):
        if child.is_dir():
            rows.append((child.name + "/", dir_size(child)))
        elif include_files and child.is_file():
            rows.append((child.name, child.stat().st_size))
    rows.sort(key=lambda row: -row[1])
    total = sum(size for _, size in rows)
    if top > 0:
        rows = rows[:top]
    width = max((len(name) for name, _ in rows), default=10)
    for name, size in rows:
        shown = human_size(size) if human else f"{size} bytes"
        bar = ""
        if total:
            bar = "#" * int(40 * size / total)
        print(f"{name:<{width}}  {shown:>12}  {bar}")
    print(f"\nTotal: {human_size(total) if human else f'{total} bytes'} "
          f"across {len(rows)} shown entr{'y' if len(rows) == 1 else 'ies'}.")


def main():
    parser = argparse.ArgumentParser(
        description="Report the size of each subfolder, largest first.")
    parser.add_argument("folder", type=Path, help="Folder to report on")
    parser.add_argument("--top", type=int, default=0,
                        help="Show only the N largest entries (0 = all)")
    parser.add_argument("--human", action="store_true",
                        help="Show sizes in KB/MB/GB instead of bytes")
    parser.add_argument("--include-files", action="store_true",
                        help="Also list files directly inside the folder")
    args = parser.parse_args()
    if not args.folder.is_dir():
        parser.error(f"not a directory: {args.folder}")
    report(args.folder, args.top, args.human, args.include_files)


if __name__ == "__main__":
    main()
