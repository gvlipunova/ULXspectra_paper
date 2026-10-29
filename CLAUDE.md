# ULXspectra_paper: instructions for Claude

A manuscript on the physical model of ULX spectra computed by the code in
`ULXspectra` (super-Eddington disc with an optically thick wind around a BH,
or around a NS with a magnetosphere), and on the fits to observed SEDs. To
be shared with colleagues; synced with Overleaf through GitHub.

## Sources

The code repository is the reference for the physics:
`/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra`
(branch `fix-results-integrity`). Start a session with
`claude --add-dir /aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra`.

Read, in this order:
1. `README.md`, section "Model Physics": the model step by step. Its
   subsections map onto `sections/` (see the comment at the top of each).
2. `CHANGELOG.md`: what changed when, with the effect on the spectra.
3. `docs/wind_velocity_laws.md`, `docs/wind_column_angles.md`: detailed
   derivations and tests, with figure scripts in `docs/scripts/`.
4. `PLAN.md`: the reasoning and the author's decisions (items C8-C17,
   section 7 for the fitting procedure).
Open the source files (`csrcs/*.c`, `psrcs/*.py`) only to check an
equation or a number.

Never edit the code repository from here.

## Rules

- **Physics decisions are the author's.** Describe the model as it is in
  the code; where the text needs a choice, an approximation or a
  justification that the sources don't give, ask, don't invent one.
- **Every equation is traceable.** After each displayed equation put a
  comment with its source, e.g. `% code: csrcs/wind_surface.c
  tau_perpendicular_simple_scalar(); README "Wind temperature"`.
- **References:** only papers the author or the sources name. Never invent
  bibliographic details; mark anything unverified with `% VERIFY` in
  `refs.bib`.
- **Numbers** (effects, fit results) come from the sources; give the code
  commit they refer to in a comment.
- **Figures** are made by scripts in the code repository (or added to it),
  never by hand; `figures/README.md` lists script and commit for each.
- **LaTeX style:** one sentence per line (clean diffs in git and Overleaf);
  `\label{eq:...}`, `\label{sec:...}`, `\label{fig:...}`; symbols as in the
  README (R_sph, R_trap, x = R/r_in, ṁ = Ṁ/Ṁ_Edd, ...). Outline items in
  the section files are comments starting with `% OUTLINE:`.
- Commit only the author's requested changes; push only when asked.
