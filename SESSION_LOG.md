# Session Log -- March 20, 2026

## What was done

Starting from the initial Overleaf import, the proposal was comprehensively
revised through an extended AI-assisted editing session. Key changes:

1. **Scientific review** against 17 reference papers; verified correctness of
   all claims, citations, and methodology.
2. **Title** changed to "Machine-Learning Identification of Dynamic Interfacial
   Motifs Governing Plastic Response" to reflect that motifs combine structure
   and motion.
3. **Structure** aligned with the companion proposal (Ran's) -- added dedicated
   sections for Research Hypothesis, Proposed Use of AI, and Data Scope.
4. **Figure** (`graphs/pipeline.pdf`) regenerated via
   `code_for_graphs/make_pipeline_fig.py`; resized, text enlarged, bold removed,
   backprop label removed.
5. **Text** shortened from 6 pages to 4 (body ~2.8 pp + references ~1.2 pp),
   tightened for directness, de-AI'd language, removed dashes, fixed orphan
   lines.
6. **References** updated: DXA reference changed to Stukowski 2012, journal
   names abbreviated, author lists capped at 3 + et al., Krief 2021/2024 added.
7. **Resource estimates** added as a condensed table (~20 runs, ~300 GiB,
   ~300 core-h MD on CPU cluster + ~100 GPU-h CNN).
8. **Timeline** converted to a compact horizontal table.
9. **Abbreviations** audited: CNN, ILDA, DDD defined; standard abbreviations
   (FCC, BCC, MD, EAM, etc.) left unexpanded.
10. **Final review** caught and fixed: GB/GiB ambiguity in table, budget line
    missing CPU cluster mention, "back stress" parallel construction.

## Current state

- `main.tex` + `references.bib` compile cleanly with `pdflatex`/`bibtex` to
  4 pages, no warnings.
- Tagged `v1.0` and pushed to `origin/main`.

## Build instructions

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

To regenerate the pipeline figure:

```bash
python3 code_for_graphs/make_pipeline_fig.py
```
