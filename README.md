## Description
Code repo for my research in July 2024.
**Report**: ./report.md

## Reproduce the results
1) Create a virtual env and install deps with uv:
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```
2) Pull data assets into `assets/` (raw + processed + topics). The full set lives at https://huggingface.co/datasets/NyaaaaaQwQ/conversational-bundles/tree/main/assets; download that folder and place it at `./assets/` so paths like `assets/raw/combat_threads_text_only.pkl` and `assets/processed/combat_threads_with_perspective.pkl` exist.
3) Run notebooks in order (01→06) via Jupyter/VS Code. Leave `DRY_RUN=True` to reuse the published artifacts, or flip to `False` to regenerate:
   - `02_generation.ipynb` expects a local Ollama endpoint (`MODEL_NAME=llama3`, `OLLAMA_ENDPOINT=http://localhost:11434/api/generate`).
   - `03_perspective.ipynb` needs `PERSPECTIVE_API_KEY` in the environment and `DRY_RUN=False` to hit the API; adjust `BATCH_LIMIT` as needed.
   - Later notebooks (`04_*`, `05_*`, `06_report`) only read processed assets and can be re-run offline once `assets/` is populated.

## Directory layout
- `old_codes`: Original code before cleaned.
- `utils/`: Shared utilities (data IO, preprocessing, LLM imitation, Perspective calls, analysis/visualization).
- `assets/`: Data and model artifacts (split into `raw/`, `processed/`, `models/`; keep placeholders for very large files when needed).
- `assets/` is also published to Hugging Face at https://huggingface.co/datasets/NyaaaaaQwQ/conversational-bundles/tree/main/assets.
- Top-level notebooks (pipeline ordered):
  - `01_data_ingest.ipynb`: Read data, extract combats, basic cleaning → `assets/raw/`
  - `02_generation.ipynb`: LLM imitation/summary/conditioning → `assets/processed/`
  - `03_perspective.ipynb`: Perspective batch scoring and cleaning → `assets/processed/`
  - `04_analysis_topics.ipynb`: BoW/TF-IDF/Count/LDA comparison (refuse vs accept)
  - `05_analysis_safety.ipynb`: Refusal rate, toxicity distribution, case filtering, visualization
  - `06_report.ipynb`: Result consolidation and report visuals
