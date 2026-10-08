# Second Brain

*Last synthesized: 2026-10-07 | 12 files | 2 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `superconducting_transformer.py`, `superconducting_transformer2.py`, `complex_leibler_transformer.py`. Architecturally it is 2 layers, dominant utility (11 files) across 2 import-based communities. Recorded risk surface: 0 security findings and 0 dependency cycles.

Surprising tissue lives between root, orphans: 0 extracted cross-community imports and 1 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (92% file coverage), 0 security findings, 0 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 12 |
| Symbols | 709 |
| Resolved imports | 2 |
| Languages | py, sh |
| Communities | 2 |
| Doc coverage | 92% (11/12 files) |
| Security findings | 0 |
| Estimated read cost | ~7956 tokens (chars/4, offline so $0) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target readmenator_Laderman_cjy_j3sq
```

## Concept Wiki

- [root (2 files, cohesion 1.00)](./community_0_root.md)
- [orphans (10 files, cohesion 0.00)](./community_1_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `superconducting_transformer.py` | 13.8 |
| `superconducting_transformer2.py` | 13.7 |
| `complex_leibler_transformer.py` | 13.1 |
| `seed_miner.py` | 9.7 |
| `laderman_crystallization.py` | 8.6 |

## Strongest Connections

- 0 -> 1: shares_context (strength 0.5, INFERRED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
