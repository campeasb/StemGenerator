import os, sys, subprocess, shutil
from pathlib import Path
from typing import Literal, Optional
import utils

def separateDemucs(input_path: Path, stems: Literal[2, 4], out_dir: Path, device: Optional[str]) -> Path:
    if stems not in (2, 4):
        raise ValueError("Stems must be 2 or 4 for Demucs")
    out_dir.mkdir(parents=True, exist_ok=True)

    tmp_out = Path(".demucs_out")
    if tmp_out.exists():
        shutil.rmtree(tmp_out)
    tmp_out.mkdir(parents=True, exist_ok=True)

    # Cache des modèles Demucs local
    env = dict(os.environ); env["DEMUCS_CACHE"] = str(Path("./demucs_models").resolve())

    # Device: "cuda" si dispo (auto), sinon "cpu"
    resolved_device = "cuda" if (device in (None, "auto") and utils.has_cuda()) else (device or "cpu")

    demucs_cmd = [
        sys.executable, "-m", "demucs.separate",
        "-n", "htdemucs_ft",
        "-o", str(tmp_out),
        "-d", resolved_device,
    ]
    if stems == 2:
        demucs_cmd += ["--two-stems", "vocals"]
    demucs_cmd.append(str(input_path))

    subprocess.run(demucs_cmd, check=True, env=env)

    model_dir = None
    for cand in tmp_out.rglob(input_path.stem):
        if cand.is_dir() and ((cand / "vocals.wav").exists() or (cand / "no_vocals.wav").exists()):
            model_dir = cand
            break

    if model_dir is None:
        shutil.rmtree(tmp_out, ignore_errors=True)
        raise RuntimeError(
            f"Demucs outputs not found for '{input_path.stem}' under {tmp_out}. "
            f"Cmd was: {' '.join(demucs_cmd)}"
        )

    # --- Dossier final: on le RÉINITIALISE pour éviter de garder d'anciens fichiers ---
    final_dir = out_dir / input_path.stem
    if final_dir.exists():
        shutil.rmtree(final_dir)
    final_dir.mkdir(parents=True, exist_ok=True)

    # --- Fichiers attendus selon 2 ou 4 stems ---
    wanted = ["vocals.wav", "no_vocals.wav"] if stems == 2 else ["vocals.wav", "drums.wav", "bass.wav", "other.wav"]

    moved = []
    for name in wanted:
        src = model_dir / name
        if src.exists():
            shutil.move(str(src), str(final_dir / name))
            moved.append(name)

    # Nettoyage du tmp
    shutil.rmtree(tmp_out, ignore_errors=True)

    if len(moved) != len(wanted):
        missing = [n for n in wanted if n not in moved]
        raise RuntimeError(f"Missing stems: {missing} in {model_dir}")

    return final_dir
