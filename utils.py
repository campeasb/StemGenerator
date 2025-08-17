import sys, subprocess, shutil
from pathlib import Path

def has_cuda() -> bool:
    try:
        r = subprocess.run(
            [sys.executable, "-c", "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)"],
            check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return r.returncode == 0
    except Exception:
        return False

def move_all_wavs(src_dir: Path, dst_dir: Path) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    for wav in src_dir.rglob("*.wav"):
        shutil.move(str(wav), str(dst_dir / wav.name))
