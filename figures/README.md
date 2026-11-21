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
| `best_fits_mc.png` | `docs/scripts/plot_best_fits_mc.py` (fit list `docs/scripts/mc_table/paper_best_fits.txt`) | `e597ba3` (branch `mc-transfer-corrections`) | Sect. Results (fig:best_fits_mc) |
| `chi2_overview.pdf` | this repository: `figures/plot_chi2_overview.py` (data: ULXspectra-mc summaries) | `e597ba3` (branch `mc-transfer-corrections`) | Sect. Results (fig:chi2_overview) |
| `chi2_all.pdf` | this repository: `figures/plot_chi2_all.py` (data: ULXspectra-mc summaries) | `e597ba3` (branch `mc-transfer-corrections`) | Sect. Results (fig:chi2_all) |
| `mass_comparison.pdf` | this repository: `figures/plot_mass_comparison.py` (data: ULXspectra-mc summaries, tab:masses) | `e597ba3` (branch `mc-transfer-corrections`) | App. Published masses (fig:masses) |
| `corrected_B_of_i.png` | this repository: `figures/ahlberg2026/plot_corrected_B.py` (data `figures/ahlberg2026/data/wind_mc.npz`) | `2272e8a` (branch `mc-transfer-corrections`) | App. Monte Carlo (fig:corrected_B) |
| `funnel_cone_vs_wind.png` | `docs/scripts/funnel_wind_cone.py` (`plot ... HolmIX alphas=45,25,10`) | `ef403b4` (branch `mc-transfer-corrections`) | App. Monte Carlo (fig:funnel_wind; replaces `funnel_beaming_vs_wind.png`) |
| `fits_by_source_mc_0p3-10keV.pdf` (6 pages) | `docs/scripts/plot_fits_by_source.py` | `8176d9c` (branch `mc-transfer-corrections`; page 6 redrawn) | App. Overview of the fits (fig:fits_M ... fig:fits_spectra) |
| `mdot_profiles.pdf` | this repository: `figures/plot_mdot_profiles.py` (schematic) | -- | Sect. Critical radii, 3.1 (fig:mdot_profiles) |
| `torque_profile.pdf`, `temperature_profile.pdf` | this repository: `figures/plot_torque_temperature.py` (from the equations of Sect. 4) | -- | App. Radial profiles (fig:torque, fig:temperature) |
| `wind_geometry.pdf` | `docs/scripts/plot_wind_geometry.py` | `65f8bbf` (branch `mc-transfer-corrections`) | Sect. Wind (fig:wind_geometry; parameters in App. A) |
| `streamlines_linear.pdf` | `docs/scripts/plot_streamlines_linear.py` | `bb66b81`, `eba4a0e` (branch `mc-transfer-corrections`) | Sect. Wind, 6.1 (fig:streamlines_linear) |
| `streamline_speed.pdf`, `streamline_speed_beta1.pdf` | `docs/scripts/plot_streamline_speed.py` | `eba4a0e`, `afb2f1f` | Sect. Wind, 6.3 (fig:streamline_speed, fig:streamline_speed_beta1) |

The two `ahlberg_published_*` figures compare with the published figures of Ahlberg et al. (2026);
their scripts are in `figures/ahlberg2026/` of this repository, not in the code repository
(see `figures/ahlberg2026/README.md`).
