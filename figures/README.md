# Figures

Each figure is made by a script in the ULXspectra code repository. List
here: file, script, code commit, and the section that uses it.

| File | Script (ULXspectra) | Commit | Used in |
|---|---|---|---|
| (candidate) `wind_column_angles.png` | `docs/scripts/compare_wind_column_angles.py` | `b6a9964` | Sect. wind temperature |
| `mc_green_surface_spectra.png` | `docs/scripts/mc_green_surface.py`, `docs/scripts/mc_green_surface_spectra.py` | `fa567f9` (unchanged at `4da7c04`) | App. Monte Carlo (fig:mc_spectra) |
| `funnel_beaming_validation.png` | `docs/scripts/funnel_beaming_mc.py` | `4da7c04` | App. Monte Carlo (fig:funnel_validation) |
| `funnel_beaming_vs_wind.png` | `docs/scripts/funnel_beaming_mc.py` | `4da7c04` | App. Monte Carlo (fig:funnel_wind) |
| `funnel_beaming_by_radius.png` | `docs/scripts/funnel_beaming_mc.py` | `4da7c04` | App. Monte Carlo (fig:funnel_radius) |
| `ahlberg_published_vs_cone_mc.png` | this repository: `figures/ahlberg2026/run_all.sh` (uses `docs/scripts/funnel_beaming_mc.py`) | `2272e8a` (branch `mc-transfer-corrections`) | App. Monte Carlo (fig:funnel_published) |
| `ahlberg_published_vs_mc_transfer.png` | this repository: `figures/ahlberg2026/run_all.sh` (uses `docs/scripts/mc_green_surface.py` and the C model); step 4 rerun 2026-11-28 with `wind_mc_c32.npz` | MC `2272e8a`, model curves `07db0f3` (branch `mc-transfer-corrections`; v0: `2272e8a`) | App. Monte Carlo (fig:mc_transfer_ahlberg) |
| `HolmIX_mc_vs_nomc_BH3a.pdf` | `docs/scripts/plot_mc_vs_nomc.py` (one-preset mode, `BH3a`; runs mc28 and nomc32) | `e13c491` (branch `mc-transfer-corrections`; v0: `e402ace`) | App. D.11 (fig:holmix_mcnomc), cited in Sects. 5 and Results |
| `visibility.pdf`, `visibility_transfer.pdf` | `docs/scripts/plot_visibility.py` (fit NGC5408 BH3a, mc28_0p3-10keV) | `0075085` (visibility.pdf), `07db0f3` (visibility_transfer.pdf, 200-run table; v0: `d186025`) | Sect. 5 (fig:visibility), Sect. 5.1 (fig:visibility_transfer) |
| `wind_ring_spectrum.pdf` | this repository: `figures/plot_wind_ring_spectrum.py` (from Eqs. fcor, Inu_wind) | -- | Sect. 5 (fig:wind_ring_spectrum) |
| `best_fits_mc.png` | `docs/scripts/plot_best_fits_mc.py` (fit list `docs/scripts/mc_table/paper_best_fits.txt` = Table 6) | `f41efec` (branch `mc-transfer-corrections`; final round; v0: `e597ba3`) | Sect. Results (fig:best_fits_mc) |
| `chi2_overview.pdf` | this repository: `figures/plot_chi2_overview.py` with `figures/final_round_data.py` (data: ULXspectra-mc `summaries/final_round_*.tsv`; presets ULX.conf.example b8e8f07) | `9fc8e3c` (branch `mc-transfer-corrections`; final round, 2026-11-28; v0: `e597ba3`) | Sect. Results (fig:chi2_overview) |
| `chi2_all.pdf` | this repository: `figures/plot_chi2_all.py` with `figures/final_round_data.py` (data: ULXspectra-mc `summaries/final_round_all_fits.tsv`) | `9fc8e3c` (branch `mc-transfer-corrections`; final round, 2026-11-28; v0: `e597ba3`) | Sect. Results (fig:chi2_all) |
| `mass_comparison.pdf` | this repository: `figures/plot_mass_comparison.py` with `figures/final_round_data.py` (data: ULXspectra-mc `summaries/final_round_best_per_source.tsv`, tab:masses) | `9fc8e3c` (branch `mc-transfer-corrections`; final round, 2026-11-28; v0: `e597ba3`) | App. Published masses (fig:masses) |
| `corrected_B_of_i.png` | this repository: `figures/ahlberg2026/plot_corrected_B.py` (data `figures/ahlberg2026/data/wind_mc.npz` = ULXspectra-mc `docs/data/ahlberg2026/wind_mc_c32.npz`, 62050f6) | MC `2272e8a`, model curves `07db0f3` (200-run table; v0: `2272e8a`) | App. Monte Carlo (fig:corrected_B) |
| `funnel_cone_vs_wind.png` | `docs/scripts/funnel_wind_cone.py` (`plot ... HolmIX alphas=45,25,10`) | `ef403b4` (branch `mc-transfer-corrections`) | App. Monte Carlo (fig:funnel_wind; replaces `funnel_beaming_vs_wind.png`) |
| `fits_by_source_final_both.pdf` (6 pages) | `docs/scripts/plot_fits_by_source.py final both` (NGC247SS in two panels, author 2026-11-28) | `9fc8e3c` (branch `mc-transfer-corrections`; v0: `fits_by_source_mc_0p3-10keV.pdf`, `8176d9c`) | App. Overview of the fits (fig:fits_M ... fig:fits_spectra) |
| `mdot_profiles.pdf` | this repository: `figures/plot_mdot_profiles.py` (schematic) | -- | Sect. Critical radii, 3.1 (fig:mdot_profiles) |
| `torque_profile.pdf` | this repository: `figures/plot_torque_temperature.py` (from the equations of Sect. 4; its `temperature_profile.pdf` is no longer used) | -- | App. Radial profiles (fig:torque) |
| `temperatures.pdf` | ULXspectra-mc `docs/scripts/plot_temperatures.py` (fit NGC5408 BH3a, mc28_0p3-10keV) | `0075085` | Sect. 4.3 (fig:temperatures) |
| `wind_geometry.pdf` | `docs/scripts/plot_wind_geometry.py` | `65f8bbf` (branch `mc-transfer-corrections`) | Sect. Wind (fig:wind_geometry; parameters in App. A) |
| `streamlines_linear.pdf` | `docs/scripts/plot_streamlines_linear.py` | `fa64b89` (branch `mc-transfer-corrections`; panel (a) marks R0, theta0, v_pol) | Sect. Wind, 6.1 (fig:streamlines_linear) |
| `streamline_speed_simple.pdf` | `docs/scripts/plot_streamline_speed.py ... simple` | `086ecf7` | App. A (fig:streamline_speed; ballistic law only) |

The two `ahlberg_published_*` figures compare with the published figures of Ahlberg et al. (2026);
their scripts are in `figures/ahlberg2026/` of this repository, not in the code repository
(see `figures/ahlberg2026/README.md`).

- `slim_disc_streamlines.pdf`, `slim_disc_streamlines_columns.pdf` (fig:slim_disc, fig:slim_disc_columns; App. D, "Outlook: a slim disc"): copied from ULXspectra-mc docs/figures (commit b2dc222), made with docs/scripts/plot_slim_disc_streamlines.py 0.5 0.05; described in docs/slim_disc_geometry.md (1896e10).
