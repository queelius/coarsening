# Build the coarsening-at-random monograph PDF from LaTeX.
# Requires a pdflatex (TeX Live). Run: make
#
# The article class is deliberate: swap \documentclass for a venue style sheet
# (imsart, IEEEtran, jmlr2e, tmlr, ...) when targeting a specific venue, and the
# body should need little else. Two passes resolve the table of contents.

LATEX ?= pdflatex
STEM  := coarsening-at-random

$(STEM).pdf: $(STEM).tex refs.bib
	$(LATEX) -interaction=nonstopmode -halt-on-error $(STEM).tex
	bibtex $(STEM)
	$(LATEX) -interaction=nonstopmode -halt-on-error $(STEM).tex
	$(LATEX) -interaction=nonstopmode -halt-on-error $(STEM).tex

.PHONY: clean
clean:
	rm -f $(STEM).aux $(STEM).log $(STEM).out $(STEM).toc $(STEM).bbl $(STEM).blg

.PHONY: distclean
distclean: clean
	rm -f $(STEM).pdf
