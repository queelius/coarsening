# Build the coarsening-at-random monograph PDF from Markdown.
# Requires pandoc and a pdflatex (TeX Live). Run: make

PANDOC ?= pandoc
SRC    := coarsening-at-random.md
PDF    := coarsening-at-random.pdf

$(PDF): $(SRC) header.tex
	$(PANDOC) $(SRC) -o $(PDF) \
	  --pdf-engine=pdflatex --toc --toc-depth=3 -H header.tex \
	  -V geometry:margin=1in -V fontsize=11pt -V documentclass=article \
	  -V colorlinks=true -V linkcolor=blue -V urlcolor=blue -V toccolor=black

.PHONY: clean
clean:
	rm -f $(PDF) build.err
