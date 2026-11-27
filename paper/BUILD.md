# Build the manuscript

Use a TeX Live installation with pdfLaTeX, BibTeX and `latexmk`. From the candidate root run

```sh
cd paper
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error manuscript.tex
```

The source is `manuscript.tex` and the bibliography is `references.bib`. The command writes `manuscript.pdf` and the LaTeX log in the paper directory. To keep the distributed PDF byte-for-byte intact, copy the paper directory before rebuilding. Inspect the rebuilt pages and check the final log for undefined citations or references and layout warnings. The PDF workflow repeats the build and log check.
