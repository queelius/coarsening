# Coarsening

*A family of papers showing that six unrelated-looking data problems are the same
statistical problem, and working out what you can and cannot recover when the
data only ever arrives coarsened.*

This repository is the shared home for the `coarsening-*` program: a set of
independent papers (each its own git repo and, where published, its own Zenodo
DOI) that port one idea from reliability statistics into a range of application
fields, then state that idea once at full generality. It is not a monorepo; it is
a coordination root. Read this file for the big picture and the publication
status; read each paper's own `CLAUDE.md` for paper-specific detail.

---

## The big idea

Most of the time you do not get to observe the thing you actually care about. You
observe a *coarsening* of it: a report that has thrown away part of the truth
through a mechanism you do not fully control.

- A failed machine is sent for repair with a *set* of suspect components, not the
  one that actually failed.
- A single cell's true mRNA count is read out as a count that is often a
  spurious zero, because the sequencing protocol dropped the molecule.
- A confidential statistic is released only after deliberate noise is added for
  privacy.
- A training label is replaced by a *vote* of cheap, noisy heuristics.
- A patient's true clinical state is visible only through the billing codes a
  coder happened to enter.
- An image's per-region labels are collapsed into one bag-level label.

These look like six different fields with six different toolkits. They are not.
Each one has the same measure-theoretic shape: a latent quantity, an observed
report that is a many-to-one (or noised) function of it, and an unknown
*coarsening mechanism* in between. A classical body of theory, **coarsening at
random** (CAR; Heitjan and Rubin 1991, Gill, van der Laan and Robins 1997), says
exactly when you may ignore that mechanism and fit the latent model at "face
value," and when ignoring it quietly biases everything.

The `coarsening-*` program takes that theory, sharpens it into a single
consistency-plus-identifiability result, and shows the six fields are one problem
wearing different clothes. The payoff is concrete: a remedy discovered in one
field (RNA spike-in controls, say) becomes recognizable as the *same device* in
another (gold labels, chart review, a non-private release), and a result proved
once transfers to all of them.

---

## The shape every chapter shares

Write the latent quantity `Y`, the observed report `R`, and a parameter of
interest `theta` governing the latent model. The report identifies only a
*candidate set* `c(R)` of latent values consistent with it (for set-valued
coarsening) or a noised value (for continuous coarsening). The data-generating
process factors as

```
  p(R | theta)  =  [ latent model f(Y; theta) ]  x  [ coarsening mechanism Pr(R | Y) ]
```

and the second factor is the unknown nuisance that blocks naive likelihood
inference. CAR is three conditions under which that nuisance becomes
*eliminable*, so that maximizing the "face-value" likelihood (the latent model
restricted to the candidate set, ignoring the mechanism) is legitimate:

- **C1 (support).** The truth is always inside the reported candidate set.
- **C2 (symmetry / non-informativeness).** Within a candidate set, the mechanism
  does not depend on *which* admissible value is the true one.
- **C3 (parameter-independence).** The mechanism does not depend on `theta`.

C1 and C3 are usually mild. **C2 is the fragile one**, and it is the
coarsened-data version of "missing at random." When C2 holds you may ignore the
mechanism; when it fails (the realistic case in every applied field above) the
face-value fit is biased and you need either a model of the violation or extra
information.

---

## The one result, in three parts

Across the family the same three statements recur, first proved in the
reliability setting and then stated once at the right generality in
`coarsening-synthesis`:

1. **A consistency identity.** At an interior maximum of the face-value
   likelihood, the model's fitted mean of a *coarsening-sufficient statistic*
   equals that statistic's empirical mean. This is the exponential-family
   moment-matching identity in disguise; it currently appears under five separate
   names (cell-total consistency in scRNA-seq, the spot-level identity in spatial
   deconvolution, release consistency in differential privacy, agreement
   consistency in weak supervision, code-frequency consistency in phenotyping).
   The synthesis states it once and recovers each as a corollary, honestly
   flagging two regimes: regular exponential families (clean) and location
   families (where the sample-mean form is exact only for a Gaussian kernel).

2. **A rank condition for identifiability.** The latent parameters are
   identifiable if and only if an *augmented candidate-set matrix* built from the
   observed reports has full column rank. Confounded candidate sets (some latent
   directions never separated) make this fail.

3. **A restoration device: the singleton.** When the rank condition fails, adding
   observations whose latent value is known exactly, *singletons* (candidate sets
   of size one), restores identifiability. Every field already has its singleton,
   and had not noticed it was the same object: RNA spike-ins, single-cell probes,
   gold labels, a non-private release, a chart-reviewed patient, a singleton bag.

---

## When the symmetry fails: the second pillar

The synthesis assumes C2 holds. The companion paper `coarsening-sensitivity`
develops the case that C2 does not, which is the usual case in practice. It
parametrizes the violation by a **tilt of magnitude delta** and proves two
things:

- **A sensitivity bound (partial identification).** The asymptotic bias of the
  face-value MLE is, to first order, linear in `delta` with an explicit constant:
  the inverse face-value information times the covariance of the score with the
  tilt. So the latent parameter is not point-identified but *partially*
  identified, over a region that contracts to a point as C2 is approached
  (`delta -> 0`).

- **A sample complexity for restoration.** Recovering the `r` confounded
  directions to a target accuracy takes of order `r / gamma^2` singletons, where
  `gamma` is the domain's *identification margin* (how informative one singleton
  is). This unifies, for example, the gold-set rate in weak supervision and the
  spike-in budget in scRNA-seq as one rate with a domain-specific margin.

So the two pillars answer complementary questions. Pillar 1 (synthesis): *when
coarsening is ignorable, what is recoverable, and how do you restore it if the
rank condition fails?* Pillar 2 (sensitivity): *when it is not ignorable, how
wrong is the face-value fit, and how much external data buys identification
back?*

---

## Six fields, one structure

The foundation is the reliability paper; the six rows below it are the
application ports. The "tilt" column is the form a C2 violation takes in that
field, and the "singleton" column is the device that restores identifiability.

| Domain | Latent quantity | The coarsened report | C2 violation (the tilt) | Singleton that restores it |
|---|---|---|---|---|
| **Reliability** (foundation) | which component caused failure | a candidate set of suspect components | group-structured informative masking | a resolving diagnostic (root-cause) |
| scRNA-seq | a cell's true transcript count | zero-inflated observed count (dropout) | dropout increasing in true expression | ERCC spike-in (count known by design) |
| Spatial transcriptomics | a spot's cell-type composition | pooled expression over the spot | capture efficiency varying by cell type | single-cell-resolution probe (MERFISH / seqFISH+) |
| Differential privacy | a confidential statistic | its privatized (noised) release | data-dependent mechanism (SVT, PTR) | a non-private release of the statistic |
| Weak supervision | the true label | a vector of labeling-function votes | labeling-function dependence given the label | a gold-labeled example |
| EHR phenotyping | a patient's true clinical state | the set of diagnosis / billing codes | severity-correlated coding | a chart-reviewed patient |
| Multiple instance learning | instance-level labels | the bag-level label | instance dependence within a bag | a singleton bag / instance label |

The same table read as mathematics is one consistency theorem, one rank
condition, and one restoration proposition; read as practice it is a catalogue of
which auxiliary experiment each field should run, and how much of it.

---

## How this program approaches the problem

The method is deliberately *unify, do not re-derive*:

- **State the shared result once, recover each field as a corollary.** The
  synthesis paper proves the general theorem and then spends a few lines per
  domain showing each named result is an instance, citing the sibling paper for
  the domain-specific development and validation rather than repeating it.
- **Distribution-agnostic foundation.** The reliability paper builds the
  likelihood collapse from the C1/C2/C3 conditions without committing to a
  particular component-lifetime distribution, so the structure, not a specific
  parametric family, is what transfers.
- **Make the levers explicit.** The identifiability condition (a rank condition)
  and the restoration lever (the singleton) are concrete and actionable, and the
  sensitivity to C2 violation is quantitative (a first-order bias constant and a
  sample-complexity rate), not a vague warning.
- **Be honest about the seams.** The synthesis names where the reduction is not
  clean: differential privacy lives in the location-family regime, not the
  exponential-family one, and is exact only for a Gaussian kernel; weak
  supervision reduces exactly only under a sufficiency-complete parametrization
  (the naive-Bayes label model that data programming uses does not make pairwise
  agreement indicators sufficient). A synthesis that hides its seams is not worth
  much.

The genesis is recorded in `scrna-masked-bridge-report.md`: the observation that
scRNA-seq dropout has the same measure-theoretic shape as masked-cause
reliability (a deterministic-or-noised function of a latent variable under an
unknown mechanism, with identifiability removable only by auxiliary structure)
was the bridge that suggested the whole family, and the careful conclusion that
the *identifiability and misspecification* results transfer while the
survival-analysis machinery (min-of-components, hazards) does not.

---

## What the approach buys, and what it does not

**Strengths.**

- *Economy and transfer.* One proof serves six fields; a remedy or diagnostic
  found in one becomes portable to the others.
- *Actionable identifiability.* The rank condition and the singleton give a
  practitioner a concrete test ("are my candidate sets confounded?") and a
  concrete fix ("collect this many singletons"), and Pillar 2 turns the fix into
  a budget via the `r / gamma^2` rate.
- *Quantitative sensitivity.* Where most applied fields treat the C2 / MNAR
  question as a binary worry, the program gives a first-order bias formula and a
  partial-identification region.
- *Honesty.* The framework states its own regimes and seams rather than
  overclaiming a uniform reduction.

**Limitations.**

- *Not new mathematics, by design.* The core identity is textbook
  exponential-family moment matching and the CAR conditions are classical; the
  contribution is organizational. That is a real contribution, but it sets the
  bar at clarity and reach, not at a new theorem.
- *Parametric face-value model.* The clean consistency results lean on regular
  exponential families or location families. Outside those, the identity is only
  asymptotic or needs extra structure.
- *C2 is usually untestable from the observed data alone.* The sensitivity pillar
  exists precisely because you typically cannot check C2; the framework can bound
  the damage as a function of the unknown tilt, but it cannot tell you the tilt
  without external data.
- *The bias bound is local.* It is first-order in `delta`; large violations are
  outside its guarantee.
- *The restoration rate is for a stylized model.* The `r / gamma^2` result is
  proved for a linear confounded-subspace setup; real domains may depart from it.
- *Singletons can be expensive or self-defeating.* They must exist and be
  obtainable. The starkest case is differential privacy, where the "singleton" is
  a non-private release, which is exactly the thing privacy forbids; there the
  device is a thought experiment about identifiability, not a usable remedy.
- *The applications are mostly analytic instantiations plus simulation.* Only
  scRNA-seq carries real-data drivers (in `sims/scrna-bridge-sim/`). The papers
  demonstrate the shared *structure*; they are not field-by-field empirical
  bake-offs against each domain's state of the art.

---

## Where it sits in the literature

The program is a descendant of, and is in conversation with, several lineages:

- **Coarsening at random and missing data.** Heitjan and Rubin (1991), Gill, van
  der Laan and Robins (1997), Little and Rubin (2002); the testability concerns
  of Grunwald and Halpern (2003) and Jaeger (2005). C2 is the coarsened-data MAR.
- **Partial identification and MNAR sensitivity analysis.** Manski (1989) bounds,
  Tamer (2010); the selection-tilt tradition of Copas and Li (1997), Molenberghs
  et al. (2008), Daniels and Hogan (2008), and Robins, Rotnitzky and Scharfstein.
  Pillar 2's tilt is a structured sensitivity parameter in this tradition.
- **Measurement error, double sampling, verification-bias correction.** Tenenbein
  (1970), Begg and Greenes (1983), Carroll et al. (2006); the singleton is the
  validation subsample, and the Rogan and Gladen (1978) correction is the
  one-direction case.
- **Competing risks** ancestry for the reliability foundation (Tsiatis 1975,
  Meilijson 1981).
- **Domain anchors** the application papers engage directly: the scRNA-seq
  zero-inflation debate (Jiang et al. 2022), diagnostic-test and crowd-label
  models (Dawid and Skene 1979, Hui and Walter 1980), data programming and weak
  supervision (Ratner et al. 2016), spatial deconvolution (RCTD / Cable 2021, and
  the bulk-deconvolution neighbors CIBERSORTx, MuSiC, BayesPrism), differential
  privacy inference (Wasserman and Zhou 2010, Dwork and Roth 2014), and multiple
  instance learning (Dietterich et al.).

---

## Where it could go next

Honest forward directions, several of which would be genuine improvements on the
current approach:

- **Semiparametric efficiency and targeted learning.** The CAR foundation is
  literally the Gill, van der Laan and Robins setting, so the natural next step is
  influence-function / targeted-minimum-loss (TMLE-style) doubly-robust
  estimators for each coarsening estimand. That would deliver efficiency and
  robustness the current parametric face-value MLE does not, and would replace the
  "regime A / regime B" split with a single semiparametric account.
- **Global, not just local, sensitivity.** Replace the first-order tilt bound with
  sharp partial-identification regions (Manski / Tamer style) or higher-order
  expansions, so large C2 violations are covered.
- **Bayesian sensitivity.** Put a prior on the tilt instead of taking a worst-case
  bound, yielding a posterior over the partial-identification region (in the
  Daniels and Hogan spirit).
- **Flexible face-value models.** Swap parametric exponential families for neural
  density estimators or normalizing flows, enforcing the consistency identity as a
  moment constraint during training; this would connect the framework to deep
  generative scRNA-seq models (scVI, DCA) that currently lack identifiability
  guarantees.
- **Optimal and active design of singletons.** The `r / gamma^2` rate invites an
  experimental-design question: *which* singletons to collect to restore the
  confounded subspace fastest (optimal design / active learning along the deficient
  directions).
- **Causal-inference bridges.** A singleton is a perfect anchor, close in spirit to
  negative controls and proximal causal inference (Miao, Tchetgen Tchetgen) and to
  instrumental identification; importing that toolkit could generalize the
  restoration device.
- **A learning-theoretic rate.** The margin `gamma` and the `r / gamma^2` rate look
  like margin-based PAC sample complexity; a Rademacher / VC treatment of the
  coarsening class could generalize the rate beyond the stylized linear model.

---

## The papers

The framework tier is the foundational theory plus the two synthesis-level papers
(the C2-holds synthesis and its C2-violation sensitivity companion); the
application tier ports the framework to specific domains. Sibling citations use
the Zenodo *concept* DOI, which always resolves to the latest published version.

| Paper | Role | Concept DOI | Published | Primary venue | Status |
|-------|------|-------------|-----------|---------------|--------|
| `masked-causes-in-series-systems` (†) | foundational theory | 10.5281/zenodo.18725577 | yes | IEEE Trans. Reliability | ready |
| `coarsening-synthesis` | cross-domain synthesis (Pillar 1, C2 holds) | 10.5281/zenodo.20533912 | yes | Statistical Science | ready |
| `coarsening-sensitivity` | imperfect-coarsening sensitivity (Pillar 2, C2 fails) | 10.5281/zenodo.20604314 | yes | Electronic Journal of Statistics | submitted 2026-06-09 (EJS2606-023), under review |
| `mdrelax` (†) | C2-sensitivity companion (R package) | 10.5281/zenodo.20414727 | yes | Technometrics | minor-revision (near ready) |
| `scrna-coarsening` | application: scRNA-seq zero inflation | 10.5281/zenodo.20414734 | yes | Genome Biology | minor-revision |
| `weaksup-coarsening` | application: programmatic weak supervision | 10.5281/zenodo.20422888 | yes | AISTATS / UAI | minor-revision |
| `spatial-coarsening` | application: spatial deconvolution | 10.5281/zenodo.20422883 | draft | RECOMB / AISTATS / journal | minor-revision |
| `dp-coarsening` | application: differential privacy | 10.5281/zenodo.20422885 | draft | TPDP / AISTATS / JPC | minor-revision |
| `phenotype-coarsening` | application: EHR phenotyping | 10.5281/zenodo.20422890 | draft | JAMIA | minor-revision |
| `mil-coarsening` (‡) | application: multiple instance learning | 10.5281/zenodo.20502964 (draft) | draft | TMLR / JMLR | minor-revision |

(†) Symlinked from `~/github/masked/` (shared with the masked-reliability
cluster); see Layout below.

(‡) Folded into `coarsening-synthesis` as the sixth corollary (`cor:mil`) and
cited there by its concept DOI; its own Zenodo draft awaits publishing (see
Status).

---

## Status

Reviewed comprehensively 2026-06-08 (full papermill multi-agent pass; per-paper
reports under each paper's `.papermill/reviews/`). Zero Critical findings across
the family. `coarsening-sensitivity` is submitted; the others are published or in
minor revision, each with a single most-important remaining item.

**Submitted, under review.**

- `coarsening-sensitivity`: submitted to the Electronic Journal of Statistics on
  2026-06-09, manuscript **EJS2606-023**, awaiting editor assignment. Track at
  `e-publications.org/ims/submission/EJS/author/track`. Its preprint is published
  (version DOI 10.5281/zenodo.20604315; concept DOI 10.5281/zenodo.20604314
  resolves).

**Ready or near-ready (blockers are operational, not intellectual).**

- `masked-causes-in-series-systems`: ready. Action: the IEEEtran two-column
  reformat at submission.
- `coarsening-synthesis`: ready. Open thread: the mil deposit plus a synthesis
  re-version (below).
- `scrna-coarsening`: add a one-line attribution at the cell-total theorem to the
  exponential-family moment-matching identity, then the Genome Biology production
  items.
- `mdrelax`: export and demonstrate the headline robustness-interval tool
  (`ri_first_order` / `ri_simulation`), reconcile title vs Zenodo metadata, trim
  to the Technometrics page limit.

**Minor-revision (single most-important item each).**

- `weaksup-coarsening`: port the already-reproducing r-sweep panel into the
  validation section as a sample-size-versus-`r` figure.
- `spatial-coarsening`: situate the rank condition against the bulk-deconvolution
  literature (CIBERSORTx, MuSiC, BayesPrism) and NMF identifiability, and soften
  or fully demonstrate the "subsumes" claim (shown in full only for RCTD).
- `dp-coarsening`: trim to the page budget or re-target a 10-page-plus-references
  venue such as AISTATS.
- `phenotype-coarsening`: run the MIMIC-IV real-data application (blocked on
  PhysioNet credentialing) or add an interim public-dataset demonstration.
- `mil-coarsening`: fix four MUSK numbers in `sections/validation.tex` that
  contradict the deposited results file, switch hardcoded appendix theorem numbers
  to `\cref`, then complete the deposit and fold-in.

**Deposits prepared, await author publish.**

- `mil-coarsening` draft 20502965 (PDF refreshed to the number-fixed build) and a
  `coarsening-synthesis` new-version draft 20600853 (v0.2.0, under concept
  20533912, carrying the mil-folded-in PDF). Publish order: mil first so its
  concept DOI resolves, then the synthesis new version that cites it. Deposit
  state is tracked in `.zenodo_drafts.json` (regenerated from the Zenodo API).

---

## Layout

- `papers/` one directory per paper, each an independent git repo.
- `sims/scrna-bridge-sim/` shared simulation and analysis code for the scRNA-seq
  paper (published separately as `github.com/queelius/scrna-coarsening-sims`,
  Zenodo concept DOI 10.5281/zenodo.20548554).
- `scrna-masked-bridge-report.md` the original cross-domain analysis that surfaced
  the scRNA-seq bridge (the genesis of the family).
- `.zenodo_drafts.json` single source of truth for Zenodo deposit state
  (regenerate from the API; do not hand-edit). `.zenodo_upload.py` is the
  draft-deposit helper.

Two entries under `papers/` are symlinks into `~/github/masked/`, not real
directories: `masked-causes-in-series-systems` (the foundational theory) and
`mdrelax` (its C2-sensitivity companion). They are shared with the
masked-reliability cluster, whose canonical home is `~/github/masked/`, and appear
here so the family is navigable without duplicating source. Editing them at either
path touches the same git repo. Any recursive operation from this root that
follows symlinks will reach into the masked cluster; for cross-paper sweeps,
decide deliberately whether the two symlinked papers are in scope.

---

## Conventions

- No em-dash characters (U+2014) in any file (enforced by a hook). Use commas,
  colons, periods, parentheses, or the ASCII hyphen-minus.
- No vanity counts as achievement filler; describe the work, not its scale.
- Author: Alexander Towell, lex@metafunctor.com, ORCID 0000-0001-6443-9897,
  Southern Illinois University Edwardsville.
- Sibling citations use Zenodo concept DOIs so references track the latest
  published version without per-revision bibliography edits.

## Citing

Cite the specific paper you use by its concept DOI from the table above. For the
program as a whole, the natural anchors are `coarsening-synthesis` (the C2-holds
unification, 10.5281/zenodo.20533912) and `coarsening-sensitivity` (the
C2-violation companion, 10.5281/zenodo.20604314).
