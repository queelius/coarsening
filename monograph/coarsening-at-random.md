---
title: "Coarsening at Random"
subtitle: "A small monograph on masked-data identifiability across domains: the one idea, its six instances, and the papers that are still missing"
author: "Alexander Towell, Southern Illinois University Edwardsville"
date: "June 2026"
---

## 0. What this is, and why it exists

The `coarsening-*` repositories are a family of papers that all turn out to be the
same paper wearing different clothes. This document states the shared idea once, at
the generality that explains the recurrence, places each existing paper inside that
frame, and then does the thing a scattered family of preprints cannot do for itself:
it draws the boundary of the program and names the papers that are *missing*, the
gaps that, once filled, would close the framework.

It is written for two readers. The first is someone meeting the program for the
first time, who wants the whole arc in one sitting rather than ten preprints. The
second is the author, deciding what to build next, and whether the program is better
told as a swarm of short papers or as a few deep ones. (The honest answer, developed
in the coda, is the latter; this monograph is a first draft of the spine such a
consolidation would need.)

The existing pieces, by Zenodo concept DOI:

| Role | Paper | Concept DOI |
|:---------|:----------------------------------------|:------------------------|
| Foundation | `masked-causes-in-series-systems` | 10.5281/zenodo.18725577 |
| Pillar 1 (C2 holds) | `coarsening-synthesis` | 10.5281/zenodo.20533912 |
| Pillar 2 (C2 fails) | `coarsening-sensitivity` | 10.5281/zenodo.20604314 |
| C2 companion (reliability) | `mdrelax` | 10.5281/zenodo.20414727 |
| Application | `scrna-coarsening` | 10.5281/zenodo.20414734 |
| Application | `spatial-coarsening` | 10.5281/zenodo.20422883 |
| Application | `dp-coarsening` | 10.5281/zenodo.20422885 |
| Application | `weaksup-coarsening` | 10.5281/zenodo.20422888 |
| Application | `phenotype-coarsening` | 10.5281/zenodo.20422890 |
| Application | `mil-coarsening` | 10.5281/zenodo.20502964 |

---

## Part I. The one idea

### 1.1 The shape every problem shares

You rarely observe the quantity you care about. You observe a *coarsening* of it: a
report `R` that is a many-to-one or noised function of a latent `Y`, produced by a
mechanism you do not fully control, and you want a latent parameter `theta` that
governs the law of `Y`. Write the latent model `g(y; theta)` and the coarsening
channel `kappa(r | y)`. The data law factors,

```
  p(R | theta) = [ latent model g(Y; theta) ]  x  [ coarsening kappa(R | Y) ],
```

and the second factor is the nuisance that blocks naive likelihood inference. The
report defines a *candidate set* `c(R) = { y : kappa(R | y) > 0 }`, the latent
values it does not exclude: a finite set of suspects in the discrete case, a
kernel-weighted continuum in the additive-noise case.

### 1.2 The three conditions

Coarsening at random (CAR; Heitjan and Rubin 1991, Gill, van der Laan and Robins
1997) is three conditions under which the nuisance becomes *eliminable*, so that
maximizing the latent model restricted to the candidate set, the "face-value"
likelihood, is legitimate:

- **C1 (support).** The truth is always inside the reported candidate set.
- **C2 (symmetry).** Within a candidate set the mechanism does not depend on which
  admissible value is the true one. This is the coarsened-data form of "missing at
  random," and it is the fragile one.
- **C3 (parameter-independence).** The mechanism does not depend on `theta`.

### 1.3 The three results that recur

Under CAR, three statements recur in every domain. The contribution of the program
is to prove them once and recover each field's named version as a corollary.

1. **A consistency identity.** At an interior maximum of the face-value likelihood,
   the model's fitted mean of a *coarsening-sufficient statistic* equals its
   empirical mean. This is exponential-family moment matching in disguise; it
   appears under six names (cell-total, spot-level, release, agreement,
   code-frequency, bag-prevalence consistency). Its moral is uniform and
   counterintuitive: marginal-fit agreement is not evidence of unbiasedness.

2. **A rank condition.** The latent parameter is identifiable iff an
   *augmented candidate-set matrix* built from the reports has full column rank.
   Confounded directions (latent components never separated by any report) make it
   fail.

3. **A restoration device: the singleton.** When the rank condition fails, a report
   that pins the latent value to a point, a *singleton* candidate set, restores
   column rank and hence identifiability. Every field already had its singleton and
   had not noticed it was the same object.

---

## Part II. The two pillars and the foundation

### 2.1 Foundation: masked causes in series systems

The framework was born in reliability. A series system fails when its first
component fails; the cause is masked, but a candidate set of suspects is observed.
`masked-causes-in-series-systems` proves the C1-C2-C3 likelihood collapse
distribution-agnostically and the augmented-candidate-set rank theorem. Everything
downstream is this paper ported. `mdrelax` is its C2-sensitivity companion (an R
package plus paper) that quantifies what happens to reliability estimates when the
symmetry condition is relaxed.

### 2.2 Pillar 1: the C2-holds synthesis

`coarsening-synthesis` is the keystone. It states the consistency identity once
(two regimes: regular exponential family, where the identity is an exact
finite-sample equality; and location family, where it is exact at a single report
and a population first-moment identity otherwise, sharp only for the Gaussian
kernel). It states the rank condition and the singleton restoration once. It then
recovers six named domain theorems as corollaries, and it is candid about the two
seams where the reduction is not clean: differential privacy lives in the
location-family branch, not the exponential-family one; weak supervision reduces
exactly only under a sufficiency-complete parametrization, asymptotically otherwise.

### 2.3 Pillar 2: the C2-fails sensitivity theory

`coarsening-sensitivity` develops the case the synthesis assumes away. It
parametrizes the C2 violation by a *tilt of magnitude delta* and proves two things:
a first-order **sensitivity bound** (the asymptotic bias of the face-value MLE is
linear in delta with an explicit constant, the inverse face-value information times
the covariance of the score with the tilt, so the latent parameter is partially
identified over a set that contracts to a point as delta goes to zero); and a
**restoration sample complexity** (recovering the `r` confounded directions to a
target accuracy takes of order `r / gamma^2` singletons, where `gamma` is the
domain's identification margin). Pillars 1 and 2 are complementary: one says what is
recoverable when coarsening is ignorable and how to restore it; the other says how
wrong the fit is when it is not, and how much external data buys identification back.

---

## Part III. Six fields, one structure

Each application instantiates the framework by naming four objects: the latent
quantity, the coarsened report, the form a C2 violation takes (the tilt), and the
singleton that restores identifiability. The reliability foundation is the zeroth
row; the six below are the ports.

| Domain | Latent `Y` | Coarsened report `R` | C2 violation (tilt) | Singleton |
|--------|-----------|----------------------|---------------------|-----------|
| Reliability (foundation) | which component failed | candidate set of suspects | group-structured informative masking | a resolving diagnostic |
| scRNA-seq | true transcript count | zero-inflated observed count | dropout increasing in true expression | ERCC spike-in (known count) |
| Spatial transcriptomics | spot cell-type composition | pooled spot expression | capture efficiency varying by cell type | single-cell-resolution probe |
| Differential privacy | confidential statistic | privatized (noised) release | data-dependent mechanism (SVT, PTR) | a non-private release |
| Weak supervision | true label | vector of labeling-function votes | labeling-function dependence | a gold-labeled example |
| EHR phenotyping | true clinical state | set of diagnosis codes | severity-correlated coding | a chart-reviewed patient |
| Multiple instance learning | instance labels | bag (OR) label | within-bag instance dependence / firing rate | a singleton bag (instance label) |

Read as mathematics the table is one theorem, one rank condition, one restoration
proposition. Read as practice it is a catalogue of which auxiliary experiment each
field should run and how much of it: the `r / gamma^2` rate of Pillar 2 turns "collect
some gold labels / spike-ins / chart reviews" into a budget with a domain-specific
margin.

The instances are not equally clean, and the program says so. scRNA-seq, spatial,
phenotyping, and MIL sit in the exponential-family regime where the consistency
identity is exact. Differential privacy sits in the location-family branch (its
"singleton," a non-private release, is the device that *defeats* privacy, so it is a
thought experiment about identifiability, not a usable remedy). Weak supervision is
exact only under a parametrization practitioners do not use.

---

## Part IV. The gaps: papers that are missing

This is the part a scattered family cannot write about itself. The program as it
stands answers "when is the latent parameter identifiable, what is recoverable, and
how does a singleton restore it." It leaves whole questions untouched. Each gap
below is stated as a paper that could be written, with the result it would establish
and its relation to what exists. They are ordered by how much they would strengthen
the spine.

### Tier 1: structural gaps that change the foundation

**G1. The semiparametric-efficiency pillar (the biggest gap).**
The entire program estimates by parametric face-value MLE. But CAR *is* the Gill, van
der Laan and Robins setting, the home of semiparametric efficiency and targeted
learning. The missing paper develops the influence-function / efficient-score and
targeted-minimum-loss (TMLE-style) doubly-robust estimator for the coarsening
estimand. Payoff: efficiency and robustness the current MLE lacks; a single
semiparametric account that *dissolves* the awkward "regime A / regime B" split of
the synthesis (both become one efficient-influence-function statement); and the right
language for nuisance estimation when the coarsening channel must itself be modeled.
This is the paper that would move the program from "a recurring identity" to "the
efficient theory of coarsened-data estimation." High difficulty, highest value.

**G2. Estimating the identifiability geometry `(r, gamma)` from data.**
Pillars 1 and 2 *assume* the confounded dimension `r` and the margin `gamma` are
known. They are not: in practice the candidate-set geometry is itself estimated. The
weak-supervision paper already flags "estimating the degeneracy dimension `r` from
data" as open; it is open everywhere. The missing paper turns the rank condition and
the margin into *estimable quantities* with their own sampling theory: a consistent
estimator of the rank deficit, a confidence statement on `gamma`, and a diagnostic a
practitioner runs before trusting any instance-level or latent output. Without this,
the `r / gamma^2` budget is not operational. Medium-high difficulty, very high value
(it is what makes the whole program usable rather than diagnostic).

**G3. Optimal and active design of singletons.**
The program identifies the singleton as the universal remedy but never optimizes its
allocation. The `r / gamma^2` rate is a *given-the-design* statement; the missing
paper asks the design question: which singletons to collect, in what proportion, to
restore the confounded subspace fastest. This is optimal experimental design and
active learning along the deficient directions, with the per-domain cost structure
(a chart review is expensive, a spike-in is cheap) entering the objective. It
converts the singleton from "a device that works" into "a budget you optimize."
Medium difficulty, high value, and unusually practical.

### Tier 2: natural extensions of the existing pillars

**G4. Global (non-local) sensitivity and sharp partial-identification regions.**
Pillar 2's bias bound is first-order in delta: local. For large C2 violations it
says nothing. The missing paper computes *sharp* partial-identification regions
(Manski / Tamer style) or higher-order expansions, so the partial-ID set is exact
rather than a first-order ellipse. This is "Pillar 2 at finite delta."

**G5. Bayesian coarsening and Bayesian sensitivity.**
Everything is frequentist MLE. The missing paper puts a prior on the tilt instead of
a worst-case bound (Daniels and Hogan spirit), yielding a posterior over the
partial-ID region, and develops the Bayesian analogue of the consistency identity
(posterior moment matching) and of the singleton (informative auxiliary likelihood).
It also gives the program a natural account of *how much* a practitioner believes C2.

**G6. Nonparametric and neural face-value models.**
The clean results lean on exponential or location families. The missing paper
replaces the parametric face-value model with a neural density estimator or
normalizing flow, enforcing the consistency identity as a moment constraint during
training, and asks when identifiability survives. This is the bridge to deep
generative scRNA-seq models (scVI, DCA) that currently handle dropout without
identifiability guarantees; the coarsening framework would supply the guarantee.

### Tier 3: bridges and frontier extensions

**G7. The causal-inference / proximal bridge.**
A singleton is a perfect anchor, and "an anchor that pins a latent quantity" is
close to negative controls and proximal causal inference (Miao, Tchetgen Tchetgen)
and to instrumental identification. The missing paper recasts the singleton as a
proximal/anchor variable and imports the proximal toolkit, generalizing restoration
beyond the exact-pin case to noisy anchors. This also connects coarsening to a large,
active causal-inference literature the program currently does not speak to.

**G8. A learning-theoretic rate.**
The margin `gamma` and the `r / gamma^2` rate look like margin-based PAC sample
complexity. The missing paper gives a Rademacher / VC treatment of the coarsening
hypothesis class, generalizing the rate beyond the stylized linear confounded-subspace
model and connecting to the coarse-label learnability line (Fotakis et al. 2021;
the 2026 mean-estimation-from-coarse-data work).

**G9. Multiclass and longitudinal coarsening.**
Several instances are binary (weak supervision, MIL); the reliability foundation is
time-to-event but the applications are static. Two missing papers: a general
multiclass/polytomous coarsening treatment (the weak-supervision paper flags the
multiclass extension as open), and coarsening at random for longitudinal/streaming
data (coarsened time series, time-varying dropout), which reconnects the program to
its survival-analysis origin.

### Cross-cutting gaps

**G10. A unified empirical study.**
Honest limitation: the applications are mostly analytic plus simulation; only
scRNA-seq carries real-data drivers. The missing paper runs the rank diagnostic and
the singleton-design recipe across several real datasets in different domains,
turning the framework's diagnostics into demonstrated practice. This is the paper
that answers a reviewer who says "show me it matters on data."

**G11. The impossibility / limits paper.**
The program is about when restoration *works*. It should also characterize when it
cannot: where no singleton helps (DP, where the singleton defeats the purpose), where
the rank deficit is structural and irreducible, where C2 violation is unbounded and
no finite external data restores identification. A clean negative-results paper would
sharpen the positive ones by drawing their boundary.

### The meta-gap

The most consequential missing artifact may be this monograph's mature form: a
single review/monograph that subsumes the six application notes into worked instances
of two or three substantial papers. Submitted as a swarm of short, tightly-coupled,
single-author preprints, the program invites a "least publishable unit" reading. Told
as the foundation, the two pillars, and a consolidated applications chapter, it reads
as what it is: one idea with reach. The gap list above doubles as the table of
contents for the chapters such a consolidation would still be missing.

---

## Part V. How the pieces fit

A reading order for someone entering cold:

1. **`masked-causes-in-series-systems`** for the C1-C2-C3 collapse and the rank
   theorem in their original, concrete reliability setting.
2. **`coarsening-synthesis`** for the abstraction: the one consistency identity, the
   rank condition, the singleton, and the six corollaries.
3. **One application** matched to the reader's field (scRNA-seq is the most developed
   and the only one with real data).
4. **`coarsening-sensitivity`** for what happens when C2 fails: the tilt bias bound
   and the `r / gamma^2` restoration rate.
5. **`mdrelax`** for the worked C2-relaxation in reliability, with software.

The dependency spine is: foundation -> synthesis (assumes C2) and sensitivity
(relaxes C2) in parallel -> applications instantiate both. The gaps of Part IV attach
as follows: G1, G2, G4, G5, G6 deepen the two pillars; G3 and G10 make them
operational; G7, G8, G9 extend their reach; G11 bounds them.

---

## Coda: the strategic read

A family of correct, closely-related, single-author papers submitted to selective
venues in a short window is vulnerable for reasons that have nothing to do with
whether the mathematics is right (it is): fit, perceived significance, and the
appearance of slicing one idea thin. The durable assets are intact, every result is
a published, citable preprint, and the ideas are timestamped and out in the world.
The recoverable move is to change the *unit*: fewer, deeper papers, and a monograph
or review as the flagship. The gap list is the agenda for what those deeper papers
would contain. The program is not a dead end; it is a spine with several vertebrae
still to grow, and it has been told, so far, in too many small voices instead of one.
