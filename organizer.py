import shutil
from pathlib import Path

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Archives": [".zip", ".rar", ".7z"],
    "Programs": [".exe", ".msi", ".apk"],
    "VPN": [".ovpn"],
}

SKIP = {"desktop.ini"}


def get_category(file: Path) -> str:
    ext = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def organize(folder: Path, dry_run: bool = True):
    for f in folder.iterdir():
        if not f.is_file() or f.name in SKIP:
            continue
        target_dir = folder / get_category(f)
        target = target_dir / f.name
        if target.exists():
            print("SKIP (exists):", f.name)
            continue
        if dry_run:
            print("WOULD MOVE:", f.name, "->", target_dir.name)
        else:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(f), str(target))
            print("MOVED:", f.name, "->", target_dir.name)


if __name__ == "__main__":
    organize(Path.home() / "Downloads", dry_run=True)

 