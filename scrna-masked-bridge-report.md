# scRNA-seq zero inflation vs masked-cause reliability: bridge analysis

**Anchor paper**: Jiang, Sun, Song, Li (2022), "Statistics or biology: the zero-inflation controversy about scRNA-seq data", *Genome Biology*, [doi:10.1186/s13059-022-02601-5](https://doi.org/10.1186/s13059-022-02601-5).

**User's framework**: Towell (2026, in press), *Distribution-agnostic likelihood for component reliability estimation in series systems with masked causes*; companion paper *Relaxed candidate set models* (mdrelax).

---

## Bottom line

**The hypothesis is correct at the level of measure-theoretic shape but wrong at the level of survival-analysis machinery.** Both problems share:
- A mixture observation that is a deterministic function of latent variables under an unknown observation mechanism,
- A parameter-of-interest layer (component hazards / true expression) entangled with a nuisance mechanism (candidate-set distribution / dropout-and-capture process),
- An identifiability barrier removable only by auxiliary structure (singleton candidate sets / spike-in RNA controls).

But scRNA-seq has no time-to-event semantics, no min-of-component structure, and integer-valued observation, so the hazard machinery does not transfer. The publishable contribution is the **identifiability theorem and misspecification result**, not the hazard framework.

---

## 1. The user's framework, stated precisely

From `papers/masked-causes-in-series-systems/paper.tex`:

- **Latent**: component lifetimes T_{ij} ~ f_j(·;θ_j); system lifetime T_i = min_j T_{ij}; cause K_i = argmin_j T_{ij}.
- **Observed**: D_i = (s_i, ω_i, c_i, x_i), where c_i ⊆ {1,...,m} is a candidate set.
- **Mechanism**: unknown Pr_θ{C_i=c | T_i=t, K_i=j}.
- **Likelihood (mdrelax §2)**: f(t,k,c;θ) = h_k(t;θ_k) · ∏_ℓ R_ℓ(t;θ_ℓ) · Pr_θ{C_i=c | T_i=t, K_i=k}.

The three conditions act as **eliminability conditions** for the masking distribution:
- **C1**: support. Pr{K_i ∈ C_i} = 1.
- **C2**: symmetry / non-informativeness. Pr{C_i=c | T_i=t, K_i=j} = Pr{C_i=c | T_i=t, K_i=k} for all j,k ∈ c.
- **C3**: independence of θ. Masking probability does not depend on the parameter of interest.

When all three hold, the likelihood collapses (Theorem 7) to L_i(θ) ∝ [∏_ℓ R_ℓ(t_i;θ_ℓ)] · [Σ_{j∈c_i} h_j(t_i;θ_j)].

**Theorem 8 (identifiability)**: under C1-C2-C3, parameters are identifiable iff the augmented candidate-set matrix C̃ has full column rank m.

**mdrelax extends this**:
- Under **Relaxed C2** with known informative weights π_{kc}(t), identifiability can *improve* relative to C1-C2-C3 because asymmetric weights break confounding symmetries.
- Under **Relaxed C3**, the C1-C2-C3 MLE converges to a pseudo-true value where total system hazard is consistent but per-component rates absorb the masking asymmetry.

---

## 2. The scRNA-seq problem in the user's notation

| User's framework | scRNA-seq |
|---|---|
| component j ∈ {1,...,m} | gene j ∈ {1,...,p} (per cell i) |
| component lifetime T_{ij} | true mRNA count Y_{ij} (latent), e.g. Poisson-Beta two-state model |
| component lifetime distribution f_j(·;θ_j) | gene-level expression model (Poisson/NB/Poisson-Beta) with θ_j = (switching, transcription, degradation rates) |
| min/system lifetime | **does not transfer**. No min-structure |
| component cause K_i | **does not transfer**. No single causing component per cell |
| candidate set c_i | observed-zero pattern: Z_{ij} = 𝟙{X_{ij} = 0}, where X_{ij} is observed count |
| candidate-set probability Pr_θ{C_i=c \| T_i=t, K_i=k} | dropout/capture mechanism Pr{X_{ij}=0 \| Y_{ij}=y, depth_i, GC_j} |
| **spike-in RNA control** | **= singleton candidate set**: a known-y observation that pins down the masking mechanism |
| C1 (cause in candidate set) | "if Y_{ij} = 0 then X_{ij} = 0 a.s." Biological zero is always observed as zero (trivially holds) |
| C2 (symmetric masking) | "dropout rate at observed zero does not depend on which Y value produced it". This is **MNAR-vs-MAR** in scRNA-seq, the controversy in the anchor paper |
| C3 (masking independent of θ) | "capture/dropout mechanism does not depend on true expression parameters". Debated; if dropout is a deterministic function of (Y, depth), this fails |

---

## 3. Where the analogy literally holds

**(a) Joint factorization.** Both have the same shape: f(observed, latent; θ, φ) = [latent density f(latent; θ)] × [unknown mechanism Pr(observed | latent; φ)]. The unknown second factor is what blocks naive likelihood inference in both.

**(b) Identifiability via auxiliary information.** Towell's singleton candidate sets (|c_i|=1) play the same role as scRNA-seq spike-ins: an observation where one element of the latent structure is known a priori. In Towell's setup, singletons restore identifiability when |c_i|>1 candidate sets are confounded; in scRNA-seq, spike-ins restore identifiability of the dropout mechanism because y is known by construction. The "p > 0 essential for identifiability" remark in §5.4 of `paper.tex` is exactly the same logic the anchor paper uses to argue for spike-in controls.

**(c) Misspecification, pseudo-true parameter.** mdrelax's misspecification theorem (total hazard consistently estimated under C2 violation, individual component rates absorb asymmetry) maps onto a known scRNA-seq result: total cell-wide expression is robust to dropout assumptions, but per-gene differential expression is not. The ZIFA / MAST debate has empirical observations of this without the formal misspecification analysis Towell provides.

---

## 4. Where the analogy breaks

**(a) No min/competing-risks structure.** A cell does not fail because of its weakest gene. Genes are observed jointly. System-pdf and system-hazard machinery (Theorems 1-3) does not transfer. What transfers is the masking layer alone, via the marginalization-over-latent argument in §4 of `paper.tex`.

**(b) Counts vs. continuous lifetimes.** Towell assumes absolute continuity w.r.t. Lebesgue measure (so K_i is a.s. unique). scRNA-seq is integer-valued. Density-based theorem statements need restating in terms of probability mass functions; the "almost surely a unique cause" structure does not exist.

**(c) Censoring vocabulary doesn't map.** Right/left/interval censoring of a survival time has no scRNA-seq analogue. The whole "observation type ω ∈ {E,R,L,I}" taxonomy is reliability-specific.

**(d) Hazard parametrization is the wrong vehicle.** scRNA-seq parameters (transcription rate, degradation rate, switching rates) are not hazards. The hazard h_j(t;θ_j) has no time argument in scRNA-seq. What survives is θ_j as the parameter-of-interest layer, not the hazard machinery.

**(e) Confounding structure is denser.** In Towell's reliability setting, C̃ has m columns. In scRNA-seq the analogue would have ~20,000 columns (genes), and the candidate-set structure is determined by which genes are observed-zero per cell, far less structured than diagnostic groupings. The full-column-rank condition becomes essentially trivially satisfied across cells, which means scRNA-seq non-identifiability has a different source: the within-cell mechanism (dropout depends on y), not the between-observation pattern.

---

## 5. Publishing opportunity

**The bridge literature is empty.** OpenAlex returns no paper crossing competing-risks / masked-cause identifiability with scRNA-seq zero inflation. Closest precedents:
- *Zero-inflated promotion cure rate model* (2017, finance, ~17 cites): connects cure models to zero inflation but not coarsening/masking.
- Van den Berge et al. (2018, Genome Biology), *"Observation weights unlock bulk RNA-seq tools for zero inflation"*: closest in spirit but does not formalize identifiability.

**Proposal sketch**: *"Coarsening-at-random conditions for scRNA-seq zero inflation: a reliability-theoretic perspective"*

> We import the C1-C2-C3 framework from masked-cause reliability inference into scRNA-seq, recasting biological-vs-non-biological zero discrimination as a coarsening problem. We show that the "glass ceiling" identified by Jiang et al. (2022) is a special case of a known identifiability theorem (Towell, 2026): observed counts alone provide rank-deficient information about latent expression parameters because biological zeros and sampling zeros enter the likelihood only through the symmetric sum that the candidate-set structure must distinguish. Spike-in RNA controls are mathematically the singleton candidate sets that restore full column rank. We provide a misspecification result paralleling mdrelax: the C2-violating "naive" zero-inflated negative binomial estimator converges to a pseudo-true value where cell-level total expression is consistent but per-gene rates absorb the dropout asymmetry.

- **Audience**: statistical genomics methodologists.
- **Venue**: *Biostatistics*, *Annals of Applied Statistics*, or methods track of *Genome Biology*.
- **Length**: ~12 pages.
- **Contribution**: conceptual unification + identifiability theorem port, not a new estimator.

---

## 6. Dependencies. What carries over

**Carries over directly:**
- Joint-distribution factorization (mdrelax §2)
- C1-C2-C3, eliminable-mechanism logic (`paper.tex` §5)
- Theorem 8 identifiability (candidate-set matrix → spike-in design matrix)
- Theorem 9 partial identifiability (block structure → cell-type-marker bundles)
- mdrelax misspecification result (pseudo-true convergence under C2 violation)
- Information-theoretic remark (Remark 1, §5.2): I(K;C_w) = ln(m/w) under uniform masking

**Code that ports cheaply:**
- `loglik`, `score`, `fit` S3 generics in `maskedcauses` are hazard-shaped, but the underlying `likelihood.model` abstraction is general. Write a new `loglik.scrna_zero_inflated` method using the same fitter machinery.
- mdrelax simulation framework for C2-violation severity sweeps ports nearly unchanged.

**New auxiliary assumptions needed:**
- Replace continuous-density assumption with PMF-valued analogues; re-derive Theorem 4 for discrete observations.
- Specify a parametric family for the dropout mechanism (logistic on log-y, or Bernoulli on capture efficiency).
- Add an explicit gene-cell exchangeability assumption. Towell can assume independent systems; scRNA-seq has gene-gene correlations within a cell that have no reliability analogue and need a copula or factor model.
- Spike-in design specification: how many transcripts at how many concentrations, mirroring how Towell discusses requirements on diagnostic resolution.

**What does not carry over:** anything tied to time-to-event semantics: cumulative hazards, survival functions, four-way censoring taxonomy, Theorems 1-3 system-derivation, additive-hazard property.

---

## Files consulted

- `/home/spinoza/github/coarsening/papers/masked-causes-in-series-systems/paper.tex` (lines 600-1100: C1-C2-C3 derivation, Theorem 8)
- `/home/spinoza/github/coarsening/papers/mdrelax/theory/relaxed_candidate_set_models.tex` (lines 130-600: relaxation taxonomy, Bernoulli/rank-based informative-masking models)
- `/home/spinoza/github/coarsening/papers/mdrelax/paper/sections/introduction.tex` (misspecification framing)
- `/home/spinoza/github/rlang/maskedcauses/README.md`, `/home/spinoza/github/rlang/maskedhaz/README.md` (operational interface)
- Anchor PDF (Jiang et al. 2022) pages 1-5 and 17-19. Future Directions section explicitly states the spike-in identifiability argument.

---

*Generated by `vista:cross-referencer` agent, 2026-05-07.*
