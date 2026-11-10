#!/usr/bin/env python3
"""Reduce the Monte Carlo through the wind (output of ULXspectra docs/scripts/mc_green_surface.py,
mc_<run>_scatter[_<set>].npz) and the C model B(mu) (model_B_of_mu.py) to small tables for the figures.

Usage:  python3 reduce_wind_mc.py OUT.npz LABEL MC.npz MODEL.npz [LABEL MC.npz MODEL.npz ...]

Per label: theta_c [deg]; MC counts in 20 bins of mu; N escaped; N at mu > cos(theta_c);
model mu grid, L_iso/L_total with mc_transfer = 1 and 0.
"""
import sys
import numpy as np

out, args = sys.argv[1], sys.argv[2:]
edges = np.linspace(0, 1, 21)
res = {"mu_edges": edges}
labels = []
for lab, mcf, mf in zip(args[0::3], args[1::3], args[2::3]):
    m, c = np.load(mcf), np.load(mf)
    mu = m["mu"][np.isfinite(m["mu"])]
    ctc = float(c["omega"])                       # omega_frac = cos(theta_c)
    res[f"{lab}:theta_c"] = np.degrees(np.arccos(ctc))
    res[f"{lab}:mc_counts"] = np.histogram(mu, edges)[0]
    res[f"{lab}:mc_in"] = np.array([np.sum(mu > ctc), mu.size])
    res[f"{lab}:mu"] = c["mu"]
    res[f"{lab}:B1"] = c["L1"] / c["Lemit1"]
    res[f"{lab}:B0"] = c["L0"] / c["Lemit0"]
    labels.append(lab)
    print(lab, f"theta_c = {res[f'{lab}:theta_c']:.1f}", "N =", mu.size)
res["labels"] = np.array(labels)
np.savez_compressed(out, **res)
