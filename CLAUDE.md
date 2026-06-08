# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This directory (`~/github/coarsening/`) is the shared home for a family of papers
that port one statistical idea, identifiability under coarsening at random (the
C1/C2/C3 conditions, after Heitjan-Rubin 1991 and Gill-van der Laan-Robins 1997),
from reliability statistics to several application domains. It is NOT a monorepo:
each paper under `papers/` is its own independent git repository with its own
GitHub remote and (where published) its own Zenodo DOI. This directory groups
them for cross-paper work and publication coordination.

This root is itself a small umbrella git repo (`github.com/queelius/coarsening`,
public) tracking ONLY the coordination files (this file, `README.md`,
`scrna-masked-bridge-report.md`, `.zenodo_drafts.json`, `.zenodo_upload.py`).
`papers/` and `sims/` are gitignored, so each paper and the simulation backend
keeps full `.git` independence (no submodules). Commit coordination-file changes
here; commit paper changes in each paper's own repo. Internal notes
(`.ecosystem/`) and Zenodo support drafts stay local (gitignored).

`README.md` is the human-facing publication tracker (per-paper DOIs, venues,
review verdicts, remaining work). Read it for status; read this file for how to
operate. Each paper also has its own `CLAUDE.md`; consult that for paper-specific
detail rather than duplicating it here.

## The intellectual structure (why the papers relate)

One shared result recurs across the family under six domain names: a
consistency identity at the MLE (the fitted marginal of a coarsening-sufficient
statistic equals its empirical mean at an interior optimum). `coarsening-synthesis`
states it once and recovers each domain version as a corollary; it also carries
the general augmented-candidate-set rank condition and the singleton-candidate-set
restoration result. Each application paper instantiates the framework with a
domain-specific "singleton candidate set" (the device that restores
identifiability): ERCC spike-ins (scrna), single-cell-resolution probes
(spatial), gold labels (weaksup), a non-private release (dp), chart review
(phenotype), and singleton bags / instance-level labels (mil). The synthesis
formalizes all six application corollaries, including `cor:mil` (added
2026-06-08), cited by mil's Zenodo concept DOI 10.5281/zenodo.20502964. mil's
Zenodo draft (20502965) and a synthesis v0.2.0 new-version draft (20600853) are
prepared and await the author's publish (mil first); see `README.md` and
`.zenodo_drafts.json`. When editing one paper's consistency or identifiability result,
check whether the synthesis paper's general statement and the sibling corollaries
stay consistent.

`masked-causes-in-series-systems` is the foundational theory both this family and
the separate masked-reliability cluster build on; `mdrelax` is its
C2-sensitivity companion. Sibling bibliographies cite each other (and the
masked-cluster k-out-of-m paper as `towell2026binary`) by Zenodo CONCEPT DOI, not
version DOI, so a citation always resolves to the latest published version
without per-revision bib edits. Preserve that convention: when adding a sibling
cite, use the concept DOI listed in `README.md`.

## Symlinks: two papers live elsewhere

`papers/masked-causes-in-series-systems` and `papers/mdrelax` are SYMLINKS into
`../../masked/` (the masked-reliability cluster's canonical home), not real
directories. Editing them at either path touches the same git repo. Consequence:
any recursive operation launched from the coarsening root that follows symlinks
(a bulk `git` loop, a global find-and-replace, `grep -r` without `-P`-scoped
excludes) will reach into `~/github/masked/`. For per-paper work this is
transparent; for cross-paper sweeps, decide deliberately whether the two
symlinked papers (and, through them, the masked cluster) are in scope.

## Building papers

Build target VARIES by paper; using the wrong one fails:

- Most papers (`coarsening-synthesis`, `dp-coarsening`, `scrna-coarsening`,
  `spatial-coarsening`, `weaksup-coarsening`, `phenotype-coarsening`):
  `cd papers/<name> && make paper`
- `masked-causes-in-series-systems`: `cd papers/masked-causes-in-series-systems
  && make pdf` (target is `pdf`/`all`, not `paper`).
- `mdrelax` is an R package; its manuscript is in the `paper/` subdir:
  `cd papers/mdrelax/paper && make pdf`.

All Makefile recipes run the full `pdflatex; bibtex; pdflatex; pdflatex`
sequence. `coarsening-synthesis` uses the IMS `imsart` class (the class files are
vendored in the repo). Verify a build with `grep -ci undefined <stem>.log`
(expect 0) rather than trusting exit code alone.

## Simulation / analysis code

`sims/scrna-bridge-sim/` is the computational backend for `scrna-coarsening`
(its own published repo, `github.com/queelius/scrna-coarsening-sims`, Zenodo
10.5281/zenodo.20548554). Base-R simulation studies (`sim.R` plus `run_v*.R`
drivers) need no external data; the real-data drivers (`run_v8`/`run_v10`
Tabula Muris, `run_v11*` Klein DECENT) need public datasets that are gitignored,
not redistributed (figshare 10.6084/m9.figshare.5715040 and GEO GSE65525; see
that repo's README). scrna analysis scripts hardcode
`SIM_DIR <- ".../coarsening/sims/scrna-bridge-sim"`; if this tree moves, those
absolute paths break and must be updated.

## Writing conventions (enforced)

- NO em-dash characters (U+2014) in any file write. A soul-plugin hook BLOCKS the
  write. Use commas, colons, periods, or parentheses; ASCII hyphen-minus is fine.
- NO vanity counts as achievement filler ("12-page paper", "spanning 40
  references"). Describe the work content, not its scale. Ordinary enumeration of
  contributions or theorems is fine.
- Author identity for all papers: Alexander Towell, lex@metafunctor.com, ORCID
  0000-0001-6443-9897, Southern Illinois University Edwardsville.

## Papermill workflow

Each paper carries a `.papermill/` directory: `state.md` (stage, thesis, venue,
contributions) and dated `reviews/<date>/` from multi-agent editorial passes
(per-specialist files plus a unified `review.md`). When reviewing, write a new
dated directory; do NOT rewrite historical review records or stale `state.md`
snapshots (they are point-in-time logs). When fixing review findings, the
unified `review.md` lists each paper's single most-important remaining item.

## Zenodo deposits (irreversible; handle carefully)

`.zenodo_drafts.json` is the single source of truth for deposit state; regenerate
it from the Zenodo API rather than hand-editing. `.zenodo_upload.py` creates
DRAFT depositions only (the author publishes via the web UI or an explicit
authorized step). Publishing a Zenodo record is irreversible (a published DOI
cannot be deleted via API, only superseded by a new version). Before any deposit
mutation: enumerate existing records from the API to avoid creating duplicates
(prior sessions created duplicate published records, noted in
`.zenodo_support_request_*.md`), mutate one record at a time, and read each back
to verify by embedded content before proceeding. To update an already-published
paper, create a new version under its existing concept DOI, do not deposit a
fresh record.
