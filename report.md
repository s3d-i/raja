# Characterizing LLM Refusal Behavior in Adversarial Multi-turn Dialogues: A Multi-scale Analysis with Perspective Safety Signals and Topic Modeling

## Motivation
Most LLM safety probes rely on single-turn synthetic prompts, yet real-world risk often escalates over multi-turn adversarial exchanges (stance attacks, insults, threats). At the same time, frontier models are larger, weights are closed, and access is typically limited to hosted endpoints—forcing a black-box assumption: we only observe outputs at given parameters and must infer alignment behavior externally. The project reframes refusal as a measurable behavior emerging from Reddit combative dialogues (≥3 turns) and pairs it with external safety proxies (Perspective API) plus topic structure. Heuristics (imm_1_check, true_rate thresholds) act as operational detectors for whether the model’s safety/alignment guardrails were hit. The goal is to tell whether refusals are principled safety responses or brittle, context-dependent glitches.

## Problem Definition
- Refusal–Safety Coupling: Is refusal aligned with external toxicity/safety attributes (e.g., TOXICITY, THREAT, IDENTITY_ATTACK) instead of random or keyword-driven triggers?
- Refusal–Topic Structure: Do refusal-heavy conversations occupy distinct topics compared with acceptance conversations?
- Turn vs Conversation Effects: Is refusal an immediate utterance reaction or driven by conversation-level risk accumulation?

## Hypotheses
- **H1 (Behavior–Toxicity Coupling):** Refused outputs occur on turns with higher Perspective risk (esp. TOXICITY/SEVERE_TOXICITY/THREAT/INSULT); quantify as mean deltas Δ = refuse − accept.
- **H2 (Conversation-level Accumulation):** Aggregating by refusal share, refusal-heavy conversations carry higher overall toxicity; risk is tied to dialogue trajectory, not a single line.
- **H3 (Topic Separability):** Refusal-heavy conversations are separable in topic space (Count/TF-IDF + LDA) from acceptance conversations.
- **H4 (Attribute Non-equivalence):** Refusal aligns more strongly with select attributes (e.g., THREAT, IDENTITY_ATTACK) than others.

## Method and Experimental Design
1) **Data construction (01_data_ingest.ipynb):** Copy convokit A↔B combat sub-dialogues (`combat_threads_text_only.pkl`, 6,842 conversations) into `assets/raw/`; keep list-of-DataFrames structure and helpers (`flatten_conversation_bundles`, `describe_bundle`) in `utils/data_io.py`.
2) **Model behavior sampling (02_generation.ipynb):** Local Llama3 via Ollama (`http://localhost:11434/api/generate`) produces turn-level imitations with a JSON marker `{"--IMMITATION--": ...}`; `imm_1_check` flags parse success. Refusal = `~imm_1_check`; dry-run echoes source text to avoid API dependency.
3) **Safety proxy (03_perspective.ipynb):** Perspective API scorer with retries/backoff over 20 attributes; dry-run stub keeps structure when offline. Scores stored as dicts or list-encoded (`perspective_ls`) and later flattened to `persp_*` columns; optional parquet export for joins.
4) **Topic analysis (04_analysis_topics.ipynb):** Collapse each conversation to a document, tag refusal-heavy when refusal_rate > `REFUSAL_THRESHOLD = 0.1`, and reuse migrated LDA assets (Count/TF-IDF) rather than recomputing. Switch `TEXT_COLUMN` between original text and model outputs.
5) **Safety analysis (05_analysis_safety.ipynb):** Compare Perspective means across refused vs accepted turns, compute deltas, and bucket high-toxicity turns using `HIGH_TOXICITY = 0.5`. Conversations marked refusal-heavy when share > `REFUSAL_CONVERSATION_THRESHOLD = 0.1`; `more_refuse` variant defines refusal via `true_rate < 0.67`.
6) **Report consolidation (06_report.ipynb):** Load processed bundle (prefers `combat_threads_with_perspective_list_more_refuse_cleaned.pkl`), derive refusal via `true_rate < 0.67`, flatten Perspective scores, compute summary metrics, pull best LDA runs (picked by coherence/perplexity), and emit `report/report_more_refuse.json`.

## Current Snapshot (more_refuse bundle)
- Dataset coverage: 35,116 turns scored; refusal share 8.91% of turns; 27.97% of conversations exceed the 0.1 refusal-share threshold.
- Toxicity: High-toxicity rate (Perspective TOXICITY ≥ 0.5) is 5.66% overall; 22.68% for refused turns vs 3.99% for accepted turns (supports H1 and H2 that refusals concentrate where risk is higher).
- Topic highlights (best LDA runs):
  - Count-vector, refusal (11 topics): clusters on race/racism, Trump/muslim bans, abortion/choice, gender/sex, rape/consent, guns/police, nazi/violence, and gay/rights—indicating refusal-heavy threads center on contentious identity/violence themes.
  - Count-vector, acceptance (28 topics): more diffuse coverage—race/culture, parenting/aging, entertainment, policing/violence, driving/drugs, military/terrorism, reproductive rights, gender identity, health, geopolitics, elections, evidence/court cases, education, markets/tipping, argumentation, crime/justice, wages/tax, law/immigration, gender roles, gun control, circumcision/ethics, animals/veganism, ideology/free speech, small talk, sports, religion.
  - TF-IDF, refusal (3 topics): race/sexual violence, gaming-slang-heavy cluster, and political/ethnicity slurs—points to sharper, noisier lexical spikes in refusal corpora.
  - TF-IDF, acceptance (2 topics): general debate around gender/rights plus a noisy proper-noun cluster (handle-like tokens), consistent with broader, less adversarial content.

## Insights
- Refusal correlates with elevated external risk signals: >5x jump in high-toxicity rate for refusals vs acceptances, reinforcing H1 and conversation-level H2.
- Topic separability is observable: refusal-heavy corpora concentrate on identity conflict, violence, and political hostility, whereas acceptance spans broader civic/social themes, aligning with H3.
- Attribute asymmetry (H4) is built into the analysis via per-attribute deltas; future runs should surface which `persp_*` columns drive the largest gaps (THREAT/IDENTITY_ATTACK expected leaders).
- Multi-turn framing matters: refusal-heavy conversation buckets capture escalation patterns beyond single-turn toxicity, validating conversation-level modeling.

## Outcomes
- Reproducible notebook pipeline (01→06) covering ingestion → imitation → Perspective scoring → topic/safety analysis → report.
- Portable assets: processed bundles, flattened Perspective scores, migrated LDA topic pickles, and summary snapshot `report/report_more_refuse.json` suitable for sharing (HF-hosted assets referenced in README).
- Utilities for bundle handling and scoring (`utils/data_io.py`) keep legacy list-of-DataFrames assets usable without restructuring.

## Limits and Next Steps
- Model coverage is narrow: reliance on local llama.cpp/Ollama generations limits cross-model robustness; next step is multi-model/temperature sweeps.
- Topic module favors reuse over recomputation: migrated LDA assets save compute but cap method updates; future work can re-fit with stronger topic models or BERT-based clustering when resources allow.
- Safety proxy reliance: Perspective is a useful proxy but biased; adding human adjudication or multiple annotators would strengthen causal claims about harm.
- Refusal labeling is heuristic: `imm_1_check` and `true_rate < 0.67` operationalize refusal; a richer taxonomy (policy refusal vs inability vs non-response) plus agreement checks would reduce labeling brittleness.
- Network/compute constraints shaped scope; roadmap includes refreshing assets with larger batches (lifting `DRY_RUN`, `BATCH_LIMIT`) and expanding refusal thresholds for sensitivity analysis. Add an LLM-as-a-judge pass to classify whether safety mechanisms were triggered, giving a complementary view beyond Perspective scores.
