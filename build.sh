#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

mkdir -p compilation graphs

export TEXINPUTS="${ROOT_DIR}/compilation/local_sty//:${TEXINPUTS:-}"

python3 code_for_graphs/make_pipeline_fig.py
python3 code_for_graphs/make_pipeline_fig_robust.py

pdflatex -interaction=nonstopmode -halt-on-error -output-directory=compilation "main.tex"
bibtex "compilation/main"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=compilation "main.tex"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=compilation "main.tex"

cp "compilation/main.pdf" "main.pdf"

echo "Build complete."
echo "Main PDF: compilation/main.pdf"
echo "Root PDF: main.pdf"
echo "Graphs: graphs/pipeline.pdf, graphs/pipeline_robust.pdf"
