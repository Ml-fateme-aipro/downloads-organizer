import json
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
HISTORY = Path(__file__).parent / "last_moves.json"


def get_category(file: Path) -> str:
    ext = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def organize(folder: Path, dry_run: bool = True):
    moves = []
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
            moves.append([str(target), str(f)])
            print("MOVED:", f.name, "->", target_dir.name)
    if moves:
        HISTORY.write_text(json.dumps(moves), encoding="utf-8")


def undo():
    if not HISTORY.exists():
        print("Nothing to undo")
        return
    moves = json.loads(HISTORY.read_text(encoding="utf-8"))
    for current, original in moves:
        cur, orig = Path(current), Path(original)
        if cur.exists() and not orig.exists():
            shutil.move(str(cur), str(orig))
            print("RESTORED:", orig.name)
        else:
            print("SKIP:", cur.name)
    HISTORY.unlink()


if __name__ == "__main__":
    organize(Path.home() / "Downloads", dry_run=True)