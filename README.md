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

Skeleton: section structure and outlines (as `% OUTLINE:` comments) taken
from README "Model Physics" of `ULXspectra` at commit `5f00569`. The journal
class is not chosen yet (`article` for now).
