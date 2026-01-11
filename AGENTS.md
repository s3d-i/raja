# 清理任务目标
- 在 `cleaned/` 下重构为独立的、可跟踪的最小仓库（已 `git init`），保持数据/代码分层清晰。
- 统一存放工具函数（`utils/`）和衍生资产（`assets/`），将原仓库的 notebook 流水线拆分为若干职责明确的 notebook。
- 梳理并复用现有 pickle 资产，记录来源与用途，避免重复计算。

# 已知研究思路与框架
- 研究对象：从 convokit Reddit 语料抽取的 A↔B 互怼子对话（≥3 轮），以及对这些发言的本地 LLM（Ollama/llama.cpp）模仿/摘要输出。
- 关键步骤：
  - 对话抽取：从 convokit 会话按 reply 链生成 “combat” 级 DataFrame 列表（`combat_df_list`）。
  - 生成与拒绝：对每条发言做模仿/摘要，记录输出与是否含拒绝标记（`imm*_check`/`refuse`）。
  - 评估：用 Perspective API 计算毒性/侮辱/细腻度等分；用词袋/TF‑IDF/Count/LDA 做主题与敏感词对比（拒绝 vs 接受）。
  - 分析：统计拒绝率、毒性分布，筛案例，生成可视化与报告。

# 已知资产与来源（需迁移/复用）
- `Raja/Convo/combat_df_list.pkl`：原始互怼文本 + `agu_1` 摘要。
- `Raja/Convo/combat_df_list_imms*.pkl`：加入模仿文本 `imm`/`imm_1` 及 `imm*_check` 标记。
- `Raja/revised_convo/combat_df_list_imms_1_full.pkl`：大规模模仿结果，约 6842 条对话单元。
- `Raja/revised_convo/combat_df_list_imms_1_full_perspective*.pkl`：在上一版本基础上加入 Perspective 评分（不同清洗/过滤版本）。
- `Raja/revised_convo/lda_results_*.pkl`：LDA 与向量化的主题对比结果（拒绝/接受分组）。
- 其他：`jp_vs_cn.csv`（YouTube 评论数据，单独探索用），`llama3-tokenizer.model`（tokenizer 资源），`pthConvert.py`（模型转换脚本）。

# 待办（后续在 cleaned/ 内分阶段完成）
- 建立 notebook 骨架（数据抽取、生成、Perspective、主题/安全分析、报告）。
- 将旧 pickle 分类迁移到 `assets/raw/` 与 `assets/processed/`，并在 README 记录来源/字段。
- 提炼 `utils/` 内的共用函数（数据 IO、LLM 调用、Perspective 调用、预处理/向量化、分析可视化）。
- 编写 README 说明流程、目录、依赖与数据获取方式；完善 `.gitignore`、`requirements.txt` 或 `pyproject`。
