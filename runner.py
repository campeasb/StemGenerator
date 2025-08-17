from pathlib import Path
from typing import Literal
import separate_demucs


def separate_file(
    input_path: str,
    stems: Literal[2, 4] = 2,
    out_dir: str = "outputs",
    device: Literal["auto", "cuda", "cpu"] = "auto",
) -> str:
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    path_out = Path(out_dir)
    final_dir = separate_demucs.separateDemucs(input_path, stems=stems, out_dir=path_out, device=device)
    return str(final_dir)
