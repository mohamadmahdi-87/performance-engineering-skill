# AI and compute playbook

Use only if the target contains model inference, retrieval, numeric processing, ETL, or comparable pipelines. This module is not needed simply because the operator is an AI assistant. No external model calls, uploads, model downloads, GPU jobs, or paid runs without explicit data/cost permission.

## P47 — AI quality, latency, and cost

- **Applies:** model calls, context construction, retrieval, or inference dominate cost or task latency.
- **Steps:** 1) Record model/version, parameters, context/output sizes, retrieval steps, useful-first-output and total duration, failures, and actual usage cost where known. 2) Evaluate one change: remove irrelevant/duplicate context, load references progressively, bound outputs, cache safely, or propose a smaller model/quantization only with quality and compatibility review. 3) Keep required instructions and relevant evidence; define privacy, cache identity, tool-call, and structured-output contracts.
- **Verify:** a held-out representative task set including hard/long-context, multilingual, refusal/safety, tool-use, and schema cases; compare quality/error metrics plus token cost, latency tails, and memory. Record stochastic variation and evaluator limitations; use exact tokenizer counts if available, otherwise label estimates.
- **Risks:** omitted requirements, hallucination, context truncation, quality loss, cross-user prompt-cache leaks, provider price/version changes, hidden reasoning/output cost, and benchmarks biased toward easy prompts. Shorter prompts are not always cheaper per successful task.
- **Reverse:** restore the prior prompt/model/retrieval configuration with compatible cache versioning; preserve private evaluation data only in approved storage. Do not treat cached output as authoritative after permission or model changes.

## P48 — Compute/data-pipeline correctness

- **Applies:** numeric, vectorized, GPU, ETL, or batch transformations are expensive or memory-bound.
- **Steps:** 1) Define exact/tolerated output differences, ordering, determinism, missing-value rules, and checkpoint semantics. 2) Profile compute, transfer, serialization, and I/O separately. 3) Try bounded chunking, batching, vectorization, existing accelerators, or incremental processing one at a time; review precision/algorithm changes explicitly.
- **Verify:** trusted-reference output, numerical tolerances and edge cases (NaN, infinities, overflow), different batch sizes, deterministic expectations, restart/checkpoint recovery, skewed inputs, transfer time, peak memory, and end-to-end cost.
- **Risks:** floating-point drift, changed reduction order, GPU out-of-memory, transfer overhead exceeding gains, nondeterminism, data skew, duplicated/lost records, and incompatible checkpoints. A kernel-only speedup is not a pipeline speedup.
- **Reverse:** restore the compatible algorithm/batching configuration; resume only from validated checkpoints or replay idempotently under an approved data plan.
