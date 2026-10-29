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
