# ULXspectra_paper

Manuscript (draft) on modelling the spectra of ultraluminous X-ray sources
with a super-Eddington accretion disc and an optically thick wind (BH or
NS with a magnetosphere). The model and the fitting code are in the
`ULXspectra` repository.

## Layout

| Path | Content |
|---|---|
| `main.tex` | document, packages, title, includes the sections |
| `sections/` | one file per section, in the order of the paper |
| `refs.bib` | bibliography (natbib, author-year) |
| `figures/` | figure files; `figures/README.md` lists the script and code commit for each |
| `CLAUDE.md` | conventions for writing with Claude Code |

## Build

    latexmk -pdf main.tex

or open the project in Overleaf (Menu → GitHub → link this repository;
Overleaf pulls and pushes commits).

## Status

Two-column `article` (no journal chosen), summary at the top
(`sections/00_summary.tex`).

- Sects. 2-8 (model physics): first draft from README "Model Physics" of
  `ULXspectra` at commit `5f00569`, equations checked against `csrcs/`.
  Main model: `set_mdot_in`; P07, L99, SS73 presented as alternatives.
  Open questions for the author are comments starting with `% AUTHOR:`
  (`grep -n "AUTHOR:" sections/*.tex`).
- Physics from the author's older draft (`SEA_spectrum.zip`, kept out of the
  repository) merged where it agrees with the code; marked `% source: old manuscript`.
- Other sections: outlines only (`% OUTLINE:`).
- Sect. 11.1 (thermalisation in the wind) and Appendix D (Lipunova 1999 envelope):
  from `docs/thermalization_in_wind.md` of `ULXspectra-mc`, branch
  `mc-transfer-corrections`, commit `69b9de7`.
- Sect. 8.1 (transfer correction, `mc_transfer = 1`) and Appendix C.6-C.7 (its
  table and held-out checks): from `docs/transfer_correction_results.md` of
  `ULXspectra-mc`, commit `2272e8a` (model state `2f22b12`). Update them
  when that file's update log changes.
- Disc temperature step at R_sph (Sect. 4, eq:Tdisc), wind energy budget
  (Sect. 7.2) and diluted wind spectrum (Sect. 8, eq:Inu_wind; Sect. 11.1):
  `ULXspectra-mc`, branch `mc-transfer-corrections`, commit `f546151`
  (`eps_w_launch_only = 1`, `wind_spectrum = 1`; author 2026-11-09). The rest of
  Sects. 2-8 still follows `fix-results-integrity`.
- Appendix C (Monte Carlo test, comparison with Ahlberg et al. 2026): preliminary,
  from `docs/green_surface_monte_carlo.md` at commit `4da7c04`.

### Plan

- Sect. 9: "Where the SEDs come from". The SEDs are a SPEX model fitted to
  0.3-10 keV and extrapolated to 1e-4-100 keV; compare fits to 0.3-10 keV with
  the "full" fits, and say what each measures (reminder paragraph in place).
- Ask the coauthors: real UV/optical and hard X-ray (NuSTAR) data for the
  sources? Why `mbb` for the soft component?
- Source names: NGC1313B ("NGC1313 BD") and NGC1313H ("NGC1313 HUL").
