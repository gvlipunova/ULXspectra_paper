#!/usr/bin/env python3
"""Opaque-cone Monte Carlo of the ULXspectra code (docs/scripts/funnel_beaming_mc.py, cone_mc: Lambertian walls,
isotropic point source, mirror plane z = 0) at the (alpha, R) of Ahlberg et al. 2026, Fig. 2 and Fig. 4.

Usage:  python3 cone_mc_runs.py ULXSPECTRA_DIR data/ahlberg_fig4.npz data/cone_mc_hist.npz [N]

Per run: counts in their 500 bins of equal solid angle (mu edges 0, 0.002, ..., 1), counts in 1-deg bins of i,
the number escaping at i <= alpha, and the number of photons N (default 2e5).
"""
import sys
import numpy as np

code, fig4, out = sys.argv[1], sys.argv[2], sys.argv[3]
N = int(float(sys.argv[4])) if len(sys.argv) > 4 else 200000
sys.path.insert(0, f"{code}/docs/scripts")
import funnel_beaming_mc as fb          # noqa: E402  (its rng is seeded: default_rng(2))

s = np.load(fig4)["logR"]
mu_e = np.linspace(0, 1, 501)
i_e = np.cos(np.radians(np.arange(90, -1, -1.0)))        # mu edges of 1-deg bins in i, ascending
runs = [(a, 3.0) for a in (5, 10, 15, 20, 25)] + [(25, float(l)) for l in (1, 2, 4, 5)]
runs += [(a, float(s[j])) for a in (10, 15, 20, 25, 30, 35, 40, 45) for j in (0, 10, 21, 31, 39)]
res = {"mu_edges": mu_e, "i_edges_mu": i_e}
for a, lR in runs:
    key = f"a{a:g}_logR{lR:.4f}"
    if key in res:
        continue
    mu = fb.cone_mc(a, 10 ** lR, n=N)[0]
    mu = mu[np.isfinite(mu)]
    res[key] = np.r_[np.histogram(mu, mu_e)[0]]
    res[key + "_i"] = np.histogram(mu, i_e)[0]
    res[key + "_in"] = np.array([np.sum(mu >= np.cos(np.radians(a))), mu.size])
    print(key, "escaped", mu.size, flush=True)
np.savez_compressed(out, **res)
