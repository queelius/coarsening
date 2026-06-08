# Coarsening: the masked-data / coarsening-at-random paper family

A family of papers that ports one statistical idea, identifiability under
coarsening at random (the C1/C2/C3 conditions, after Heitjan-Rubin 1991 and
Gill-van der Laan-Robins 1997), from reliability statistics to a range of
application domains. Each paper is its own git repository with its own GitHub
remote and (where published) its own Zenodo DOI; this directory is the shared
home for focused work and publication coordination, not a monorepo.

## Layout

- `papers/` one directory per paper (each an independent git repo).
- `sims/scrna-bridge-sim/` shared simulation and analysis code for the scRNA-seq
  paper (published separately as `github.com/queelius/scrna-coarsening-sims`,
  Zenodo concept DOI 10.5281/zenodo.20548554).
- `scrna-masked-bridge-report.md` the original cross-domain analysis that
  surfaced the scRNA-seq bridge (the genesis of the family).

Two papers in `papers/` are symlinks, not real directories:

- `papers/masked-causes-in-series-systems` -> `../../masked/masked-causes-in-series-systems`
- `papers/mdrelax` -> `../../masked/mdrelax`

These are the foundational theory paper and its C2-sensitivity companion. They
are shared with the masked-reliability cluster, whose canonical home is
`~/github/masked/`, and they appear here by symlink so the coarsening family is
navigable without duplicating the source. Edit them at either path; it is the
same working tree and the same git repo. The masked cluster also contains
sibling papers not part of the coarsening family but related to the foundational
theory: `reliability-estimation-in-series-systems` (the master's-project
precursor), `masked-series-companions` (companion sub-papers), and
`binary-threshold-component-identification-k-out-of-m-systems` (the k-out-of-m
companion, cited in this family's bibliographies as `towell2026binary`).
- `.zenodo_drafts.json` single source of truth for the Zenodo deposit state
  (regenerate from the Zenodo API; do not hand-edit).
- `.zenodo_upload.py` draft-deposit helper (reads each paper's `.zenodo.json`).
- `.zenodo_support_request_*.md` drafted requests to remove two prior-session
  duplicate published records (optional; nothing cites the duplicates).

## The papers

The framework tier is the foundational theory plus the synthesis; the
application tier ports the framework to specific domains. Citation uses the
Zenodo concept DOI (resolves to the latest published version).

| Paper | Role | Concept DOI | Published | Primary venue | Review verdict |
|-------|------|-------------|-----------|---------------|----------------|
| `masked-causes-in-series-systems` (†) | foundational theory | 10.5281/zenodo.18725577 | yes | IEEE Trans. Reliability | ready (2026-06-08) |
| `coarsening-synthesis` | cross-domain synthesis | 10.5281/zenodo.20533912 | yes | Statistical Science | ready |
| `mdrelax` (†) | C2-sensitivity companion (R package) | 10.5281/zenodo.20414727 | yes | Technometrics | minor-revision (near ready) |
| `scrna-coarsening` | application: scRNA-seq zero inflation | 10.5281/zenodo.20414734 | yes | Genome Biology | minor-revision (2026-06-08) |
| `weaksup-coarsening` | application: programmatic weak supervision | 10.5281/zenodo.20422888 | yes | AISTATS / UAI | minor-revision |
| `spatial-coarsening` | application: spatial deconvolution | 10.5281/zenodo.20422883 | draft | RECOMB / AISTATS / journal | minor-revision |
| `dp-coarsening` | application: differential privacy | 10.5281/zenodo.20422885 | draft | TPDP / AISTATS / JPC | minor-revision |
| `phenotype-coarsening` | application: EHR phenotyping | 10.5281/zenodo.20422890 | draft | JAMIA | minor-revision |
| `mil-coarsening` (‡) | application: multiple instance learning | not yet deposited | draft | ML conference (TBD) | minor-revision (2026-06-08) |

(†) Symlinked from `~/github/masked/` (shared with the masked-reliability
cluster); see Layout above.

(‡) Drafted and reviewed (2026-05-26). Folded into `coarsening-synthesis` as the
sixth corollary (`cor:mil`) on 2026-06-08; still pending its own Zenodo deposit,
so the synthesis cites it by GitHub URL until a concept DOI exists. See "Folded
into the synthesis, deposit pending" under Publication status below.

The shared structural result across the family is one consistency theorem for
coarsened-data MLEs (the fitted marginal of a coarsening-sufficient statistic
equals its empirical mean at an interior MLE), stated once in the synthesis
paper and specialized to each domain; the synthesis also carries the general
augmented-candidate-set rank condition and the singleton-candidate-set
restoration result, with each domain's singleton device (ERCC spike-ins,
single-cell-resolution probes, gold labels, non-private releases, chart review)
as an instance.

## Publication status and remaining work

Reviewed comprehensively 2026-06-08 (full papermill multi-agent pass; per-paper
reports under each paper's `.papermill/reviews/2026-06-08/`, the prior pass under
`2026-06-04/`). Zero Critical findings across the family. One paper is now
`ready`; the rest are `minor-revision`, each with a single most-important item.

Ready or near-ready (blockers are operational, not intellectual):

- `masked-causes-in-series-systems`: ready (0 critical, 0 major). Action: the
  IEEEtran two-column reformat at submission to IEEE Trans. Reliability, the only
  deferred production step.
- `coarsening-synthesis`: ready. The 2026-06-08 review items (cor:mil restated as
  a true regime-(A) score corollary, the cor:dp count, the Dietterich MUSK
  anchor) are fixed; the only open thread is the mil deposit plus a synthesis
  re-version (see below).
- `scrna-coarsening`: minor-revision. Action: add a one-line attribution at the
  cell-total theorem to the standard exponential-family moment-matching identity,
  then the Genome Biology production items (data-availability section, appendix as
  Methods, APC).
- `mdrelax`: minor-revision. Action: export and demonstrate the headline
  robustness-interval tool (`ri_first_order` / `ri_simulation` are unexported);
  reconcile the title vs Zenodo metadata; trim to the Technometrics page limit.

Minor-revision (single most-important item from the 2026-06-08 review):

- `weaksup-coarsening`: port the already-reproducing r-sweep panel (in
  `.research/`) into the validation section as a sample-size-versus-r figure.
- `spatial-coarsening`: add a paragraph and a few citations situating the rank
  condition against the bulk RNA-seq deconvolution literature (CIBERSORTx, MuSiC,
  BayesPrism) and the NMF-identifiability work, and soften or fully demonstrate
  the "subsumes ..." claim (shown in full only for RCTD).
- `dp-coarsening`: trim to the page budget (the build is ~15 pages against a
  ~12-page target) or re-target a 10-page-plus-references venue such as AISTATS
  (the nearest frequentist DP-inference neighbors are now cited).
- `phenotype-coarsening`: run the MIMIC-IV real-data application (blocked on
  PhysioNet credentialing) or add an interim semi-synthetic or public-dataset
  demonstration (the Beesley-Mukherjee positioning is now resolved).
- `mil-coarsening`: fix four MUSK numbers in `sections/validation.tex` that
  contradict the deposited results file, and switch the hardcoded appendix
  theorem numbers to `\cref` (then complete the deposit and fold-in, below).

Folded into the synthesis, deposit pending (2026-06-08 pass):

- `mil-coarsening` (multiple instance learning) is now the sixth application in
  `coarsening-synthesis`: a `cor:mil` bag-prevalence consistency corollary, rows
  in the sufficient-statistic, singleton, and reach tables, an applications
  subsection, and an open-problem note. The synthesis now reads "seven domains,
  six corollaries" and builds clean (12 pages, zero undefined refs/cites). Its
  three-result structure (rank condition on the bag composition matrix,
  IRLS-weighted bag-prevalence consistency, aggregation-misspecification bias
  bound) parallels the spatial and dp papers; the singleton device is the
  singleton bag (an instance-level label). Two author steps remain: (1) deposit
  `mil-coarsening` to Zenodo for a concept DOI (it was reviewed 2026-05-26), then
  (2) replace the interim GitHub-URL cite for `towell2026milcoarsening` in the
  synthesis bib with that concept DOI and cut a new synthesis version. Until
  then the synthesis source includes mil but the published Zenodo records (both
  the synthesis and mil) do not yet reflect it.

## Conventions

- No em-dash characters (U+2014) in any file (enforced by a hook).
- No vanity counts as achievement filler; describe the work, not the scale.
- Author: Alexander Towell, lex@metafunctor.com, ORCID 0000-0001-6443-9897,
  Southern Illinois University Edwardsville.
- Sibling citations use Zenodo concept DOIs so references track the latest
  published version without per-revision bib edits.
