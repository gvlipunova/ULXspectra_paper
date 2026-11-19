Results of Ahlberg et al. 2026 (arXiv:2610.23089v1) read from the vector paths of their figures
(paper repository, figures/ahlberg2026/; extraction checks in figures/ahlberg2026/README.md).

ahlberg_fig2_B_500bins.tsv  B(i) of their figure 2 in their 500 bins of equal solid angle (d mu = 0.002).
                            Lambertian (L) and electron-scattering (Ch) walls; alpha = 5, 10, 15, 20, 25 deg at R = 1e3
                            (fig2a) and alpha = 25 deg at R = 1e1, 1e2, 1e3, 1e4, 1e5 (fig2b). NaN: below B = 0.01.
                            In all ten Lambertian curves our cone MC matches best when shifted by one bin towards the
                            axis (App. C.7, footnote); no shift is applied here.
ahlberg_fig2_B_20bins.tsv   the same averaged into 20 equal bins in mu (as Fig. 8 of the paper).
ahlberg_fig4_mean_boost.tsv mean boost at i <= alpha on their grid, alpha = 6.25-45 deg (32 values), R = 10-1e5 (40 values),
                            electron-scattering walls only.

Overlap with Fig. 8 (alpha = 45.6, 31.8, 25 deg; R = 1e2, 1e3, 1e4):
  B(i) curves: only alpha = 25 deg, R = 1e2, 1e3, 1e4 (fig2b; L and Ch). No B(i) at 31.8 or 45.6 deg.
  Mean boost: alpha = 45 deg and 31.25 deg (nearest grid values) at R ~ 1e2, 1e3, 1e4; electron-scattering walls,
  0.94-0.96 of it for Lambertian walls (their figure 2a).
Reading error: steps of figure 2 are exact path coordinates; figure 4 +-0.11 in B.
