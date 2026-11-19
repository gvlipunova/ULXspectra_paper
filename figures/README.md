# Figures

Each figure is made by a script in the ULXspectra code repository. List
here: file, script, code commit, and the section that uses it.

| File | Script (ULXspectra) | Commit | Used in |
|---|---|---|---|
| (candidate) `wind_column_angles.png` | `docs/scripts/compare_wind_column_angles.py` | `b6a9964` | Sect. wind temperature |
| (candidate) `vwind_laws.png`, `vwind_compare.png` | `docs/scripts/compare_wind_velocity_laws.py` | `35a22c0` | Sect. wind |
| `mc_green_surface_spectra.png` | `docs/scripts/mc_green_surface.py`, `docs/scripts/mc_green_surface_spectra.py` | `fa567f9` (unchanged at `4da7c04`) | App. Monte Carlo (fig:mc_spectra) |
| `funnel_beaming_validation.png` | `docs/scripts/funnel_beaming_mc.py` | `4da7c04` | App. Monte Carlo (fig:funnel_validation) |
| `funnel_beaming_vs_wind.png` | `docs/scripts/funnel_beaming_mc.py` | `4da7c04` | App. Monte Carlo (fig:funnel_wind) |
| `funnel_beaming_by_radius.png` | `docs/scripts/funnel_beaming_mc.py` | `4da7c04` | App. Monte Carlo (fig:funnel_radius) |
| `ahlberg_published_vs_cone_mc.png` | this repository: `figures/ahlberg2026/run_all.sh` (uses `docs/scripts/funnel_beaming_mc.py`) | `2272e8a` (branch `mc-transfer-corrections`) | App. Monte Carlo (fig:funnel_published) |
| `ahlberg_published_vs_mc_transfer.png` | this repository: `figures/ahlberg2026/run_all.sh` (uses `docs/scripts/mc_green_surface.py` and the C model) | `2272e8a` (branch `mc-transfer-corrections`) | App. Monte Carlo (fig:mc_transfer_ahlberg) |
| `HolmIX_mc_vs_nomc.png` | `docs/scripts/plot_mc_vs_nomc.py` | `b551655` (branch `mc-transfer-corrections`) | Sect. Results (fig:holmix_mcnomc) |
| `best_fits_mc.png` | `docs/scripts/plot_best_fits_mc.py` (fit list `docs/scripts/mc_table/paper_best_fits.txt`) | `bf192da` (branch `mc-transfer-corrections`, not yet pushed) | App. Monte Carlo (fig:best_fits_mc) |

The two `ahlberg_published_*` figures compare with the published figures of Ahlberg et al. (2026);
their scripts are in `figures/ahlberg2026/` of this repository, not in the code repository
(see `figures/ahlberg2026/README.md`).
