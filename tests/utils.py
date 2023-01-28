from pathlib import Path


def recursive_remove(path: Path):
    for p in path.glob("*"):
        if p.is_file():
            p.unlink()
        elif p.is_dir():
            recursive_remove(p)

    path.rmdir()
