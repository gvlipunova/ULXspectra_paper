#!/bin/bash
# Comparison with the published results of Ahlberg et al. 2026 (arXiv:2610.23089v1).
# Usage: bash run_all.sh PDF ULXSPECTRA_DIR WORK_DIR
#   PDF            the arXiv PDF 2610.23089v1 (not in this repository)
#   ULXSPECTRA_DIR the code, branch mc-transfer-corrections, commit 2272e8a, C library built (make -C csrcs)
#   WORK_DIR       scratch directory for the wind MC runs (about 35 MB)
# Writes data/*.npz, data/summary.txt and ../ahlberg_published_vs_{cone_mc,mc_transfer}.png.
set -e
PDF=$1; CODE=$2; W=$3
H=$(cd "$(dirname "$0")" && pwd); DATA=$H/data; mkdir -p "$DATA" "$W/runs" "$W/mc" "$W/model"

# 1. Published data, recovered from the vector PDF
python3 "$H/extract_fig2.py" "$PDF" L  "$DATA/ahlberg_fig2_L.npz"
python3 "$H/extract_fig2.py" "$PDF" Ch "$DATA/ahlberg_fig2_Ch.npz"
python3 "$H/extract_fig4.py" "$PDF" "$DATA/ahlberg_fig4.npz"

# 2. Opaque-cone MC of the code at their (alpha, R)
python3 "$H/cone_mc_runs.py" "$CODE" "$DATA/ahlberg_fig4.npz" "$DATA/cone_mc_hist.npz" 2e5

# 3. Wind: parameter sets of NGC7793 from the regression references of the code (tests/reference/*.npz)
cd "$CODE"
for p in BH3a BH4a BH2; do
  python3 "$H/make_rundir.py" "tests/reference/mcmc_NGC7793.$p.wide_1keV.npz" "$W/runs"
done
R=$W/runs
run() {  # RUNDIR [name=value]: MC through the wind (1e5 packets, scattering) and the C model B(mu)
  python3 "$H/run_mc_numpy2.py" docs/scripts/mc_green_surface.py "$1" 1e5 scatter "$W/mc" ${2:+$2}
  python3 "$H/model_B_of_mu.py" "$1" "$W/model/$(basename "$1")${2:+_$2}.npz" ${2:+$2}
}
run "$R/mcmc_NGC7793.BH3a.wide_1keV" omega_frac=0.85
run "$R/mcmc_NGC7793.BH3a.wide_1keV"
run "$R/mcmc_NGC7793.BH2.wide_1keV"
run "$R/mcmc_NGC7793.BH4a.wide_1keV"
for w in 0.5 0.3 0.1; do run "$R/mcmc_NGC7793.BH3a.wide_1keV" omega_frac=$w; done
M=$W/mc; Q=$W/model; n=mcmc_NGC7793
python3 "$H/reduce_wind_mc.py" "$DATA/wind_mc.npz" \
  "BH3a,w=0.85" "$M/mc_NGC7793.BH3a.wide_1keV_scatter_omega_frac0.85.npz" "$Q/$n.BH3a.wide_1keV_omega_frac=0.85.npz" \
  "BH3a,w=0.7"  "$M/mc_NGC7793.BH3a.wide_1keV_scatter.npz"               "$Q/$n.BH3a.wide_1keV.npz" \
  "BH2,w=0.7"   "$M/mc_NGC7793.BH2.wide_1keV_scatter.npz"                "$Q/$n.BH2.wide_1keV.npz" \
  "BH4a,w=0.513" "$M/mc_NGC7793.BH4a.wide_1keV_scatter.npz"              "$Q/$n.BH4a.wide_1keV.npz" \
  "BH3a,w=0.5"  "$M/mc_NGC7793.BH3a.wide_1keV_scatter_omega_frac0.5.npz" "$Q/$n.BH3a.wide_1keV_omega_frac=0.5.npz" \
  "BH3a,w=0.3"  "$M/mc_NGC7793.BH3a.wide_1keV_scatter_omega_frac0.3.npz" "$Q/$n.BH3a.wide_1keV_omega_frac=0.3.npz" \
  "BH3a,w=0.1"  "$M/mc_NGC7793.BH3a.wide_1keV_scatter_omega_frac0.1.npz" "$Q/$n.BH3a.wide_1keV_omega_frac=0.1.npz"

# 4. Figures and numbers
python3 "$H/plot_ahlberg_comparison.py" "$DATA" "$H/.."
