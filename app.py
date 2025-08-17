import io, zipfile, subprocess, shutil
from pathlib import Path
import streamlit as st
from runner import separate_file
import utils

st.set_page_config(page_title="Stems Separator Project", page_icon="🎧")

# ---------------- State init ----------------
if "view" not in st.session_state:
    st.session_state.view = "home"      # "home" | "results"
if "results" not in st.session_state:
    st.session_state.results = None     # {"out_dir": str, "files": [str, ...]}

# ---------------- Results Page ----------------
def render_results():
    res = st.session_state.results
    if not res:
        st.info("No results in memory."); return

    path_out = Path(res["out_dir"])
    stems = [Path(p) for p in res["files"] if Path(p).exists()]

    st.title("✅ Generated Stems")
    if not stems:
        st.error("no stems found")
        return

    for stem in stems:
        st.markdown(f"**{stem.name}**")
        st.audio(stem.read_bytes(), format="audio/wav")
        st.download_button("Download", data=stem.read_bytes(),
                           file_name=stem.name, mime="audio/wav", key=f"dl-{stem.name}")

    # ZIP all
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in stems:
            zf.write(fp, arcname=fp.name)
    buf.seek(0)
    st.download_button("Download All Stems (.ZIP)", data=buf,
                       file_name=f"{path_out.name}_stems.zip", mime="application/zip", key="dl-zip-all")

    st.divider()
    if st.button("↩️ Separate another song"):
        st.session_state.results = None
        st.session_state.view = "home"
        st.rerun()

# ---------------- Home Page ----------------
def render_home():
    st.title("Stems Separator Project : Demucs for Youtube Links")

    # Input
    youtube_url = st.text_input("Youtube Link : Music of your choice")

    # Options
    stems = st.pills("Number of Stems", [2, 4], selection_mode='single')

    # Demucs uniquement
    device = "auto"  # 'auto' => utils.has_cuda() décidera 'cuda'/'cpu'
    st.caption("Engine: Demucs")
    st.caption("Acceleration: " + ("GPU CUDA ✅" if utils.has_cuda() else "CPU ⚠️ (might take a while)"))

    # Action
    if st.button("Generate Stems"):
        if not youtube_url:
            st.warning("Please enter a valid Youtube link")
            st.stop()

        from datetime import datetime

        workdir = Path("uploads")
        if workdir.exists():
            shutil.rmtree(workdir)
        workdir.mkdir(exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = workdir / f"input_{ts}.wav"  # <-- NOM UNIQUE À CHAQUE RUN

        # Download
        st.info("Downloading Audio From Youtube...")
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "wav",
            "-o", str(audio_path),
            youtube_url
        ], check=True)

        # Separate (Demucs only)
        st.info("Generating Stems with Demucs...")
        try:
            out_dir = separate_file(
                str(audio_path),
                stems=stems,
                out_dir="outputs",
                device=device
            )
        except Exception as e:
            st.error(f"error while generating stems : {e}")
            st.stop()

        # Prepare results page and rerun to display only results
        path_out = Path(out_dir)
        files = sorted(path_out.glob("*.wav"))
        if not files:
            st.error("no stems found")
            st.stop()

        st.session_state.results = {"out_dir": str(path_out), "files": [str(p) for p in files]}
        st.session_state.view = "results"
        st.rerun()

# ---------------- Router ----------------
if st.session_state.view == "results" and st.session_state.results:
    render_results()
else:
    render_home()
