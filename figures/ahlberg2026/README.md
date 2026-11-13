# Comparison with the published results of Ahlberg et al. 2026

Ahlberg, Veledina, Churazov & Khabibullin, *Maximal efficiency of geometric beaming and
polarization of highly super-Eddington X-ray sources*, arXiv:2610.23089v1 (16 Oct 2026).

Their results are taken from their figures only, never recomputed: the figures of the PDF
are vector graphics, and the curves and grid cells are read from the drawing paths.

| Their result | Script | Data | What it is |
|---|---|---|---|
| Fig. 2a, 2b (top row, Lambertian walls) | `extract_fig2.py PDF L` | `data/ahlberg_fig2_L.npz` | B_L(i): alpha = 5-25 deg at R = 1e3; alpha = 25 deg at R = 1e1-1e5 |
| Fig. 2a, 2b (middle row, Chandrasekhar walls) | `extract_fig2.py PDF Ch` | `data/ahlberg_fig2_Ch.npz` | B_Ch(i), same cases |
| Fig. 4a, 4b | `extract_fig4.py PDF` | `data/ahlberg_fig4.npz` | B_Ch averaged over i <= alpha, and B_Ch/B_max; alpha = 6.25-45 deg, R = 10-1e5 |

Checks of the extraction:
- Fig. 2: their B(i) is tallied in 500 bins of equal solid angle (their Sect. 3.1); the
  extracted curves have their steps at mu = 0.998, 0.996, ... The integral of B over mu
  from 0 to 1 is 0.93-0.99 (1 by definition): the curves end at B = 0.01, the lower edge of the plot.
- Fig. 4: the cell colours are viridis to within 0.006 in RGB. On the contour lines of
  panel (a) (B = 4, 5, ..., 20) the recovered grid gives the contour level within 0.05.
  Resolution: +-0.11 in B (panel a), +-0.2 per cent (panel b).
  Within the paper, panel (a)/B_max exceeds panel (b) by 1-6 per cent, more at small alpha.

Our side:
- `cone_mc_runs.py`: the opaque-cone MC of the code (`docs/scripts/funnel_beaming_mc.py`,
  Lambertian walls) at their (alpha, R), 2e5 photons per run -> `data/cone_mc_hist.npz`.
- `make_rundir.py`, `run_mc_numpy2.py`, `model_B_of_mu.py`, `reduce_wind_mc.py`: Monte Carlo
  through the wind (`docs/scripts/mc_green_surface.py`, scattering, 1e5 packets) and the C model
  B(mu) with `mc_transfer` = 1 and 0, for the NGC7793 parameter sets in `tests/reference/` of
  the code (BH2, BH3a, BH4a; BH3a also with omega_frac = 0.85, 0.5, 0.3, 0.1) -> `data/wind_mc.npz`.
  `run_mc_numpy2.py` only supplies `np.trapz` (removed in numpy 2) and runs the code's script unchanged.
- `plot_ahlberg_comparison.py`: the two figures and `data/summary.txt` (all numbers quoted in App. C).

Code: ULXspectra, branch `mc-transfer-corrections`, commit `2272e8a`.
Run everything with `bash run_all.sh PDF ULXSPECTRA_DIR WORK_DIR` (the PDF is not in the repository).
