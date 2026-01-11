# 项目概览（cleaned 版）

## 研究目标
从 Reddit convokit 语料中抽取 A↔B 互怼子对话，生成 LLM 模仿/摘要，结合 Perspective 评分与主题建模，分析模型拒绝/安全性和话题差异。

## 目录规划
- `utils/`：共用工具（数据 IO、预处理、LLM/模仿、Perspective、分析可视化等）。
- `assets/`：数据与模型资产（建议再分 `raw/`、`processed/`、`models/`；大文件可只放占位说明）。
- 顶层 notebook（建议按流水线编号）：
  - `01_data_ingest.ipynb`：数据读取、combat 抽取、基础清洗 → `assets/raw/`
  - `02_generation.ipynb`：LLM 模仿/摘要/定向 → `assets/processed/`
  - `03_perspective.ipynb`：Perspective 批处理与清洗 → `assets/processed/`
  - `04_analysis_topics.ipynb`：词袋/TF‑IDF/Count/LDA 对比（拒绝 vs 接受）
  - `05_analysis_safety.ipynb`：拒绝率、毒性分布、案例筛选与可视化
  - `06_report.ipynb`：结果汇总与可视化报告

## 现有资产（待迁移/标注来源）
- `combat_df_list*.pkl` 系列：互怼文本、LLM 摘要/模仿及 `imm*_check`、`refuse` 等字段。
- `*_perspective*.pkl`：Perspective 评分版本（含不同清洗/过滤）。
- `lda_results_*.pkl`：主题/向量化结果。
- `assets/processed/topics/lda_results_*.pkl`：从 `../Raja/revised_convo/` 迁移的 TF-IDF/Count LDA 结果（refuse/accept 切分）。
- `assets/processed/combat_threads_with_perspective*.pkl`：从 `../Raja/revised_convo/combat_df_list_imms_1_full_perspective*.pkl` 迁移；包含带 Perspective 评分的模仿文本（`*_list` 版本附带 `perspective_ls`，`*_more_refuse_cleaned` 版本附带 `true_rate`/`refuse_add`）。
- `assets/processed/report/`：报告快照输出目录（由 `06_report.ipynb` 生成，默认空目录）。
- `jp_vs_cn.csv`：YouTube 评论数据（独立探索）。
- 其他：`llama3-tokenizer.model`、模型转换脚本等。

## 依赖（初稿）
见 `requirements.txt`。无需远程 API key；默认使用本地 llama.cpp / Ollama 服务。

## 后续步骤
- 梳理并迁移旧 pickle 至 `assets/`，在 README 中记录生成方式与字段。
- 提炼 `utils/` 工具模块，替换 notebook 中的重复代码。
- 在 notebook 中按顺序写出输入/输出路径、形状与产物说明，保证可复现。
