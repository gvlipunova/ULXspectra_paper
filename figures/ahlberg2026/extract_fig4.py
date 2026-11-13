#!/usr/bin/env python3
"""Recover Fig. 4 of Ahlberg et al. 2026 (arXiv:2610.23089v1) from the vector graphics of the PDF:
(a) the boost factor B_Ch averaged over i <= alpha, (b) B_Ch / B_max in per cent, Chandrasekhar walls.

Usage:  python3 extract_fig4.py 2610.23089v1.pdf OUT.npz

Each grid cell is a filled rectangle whose colour is viridis(value) on the linear colorbar range; the
value is recovered by inverting viridis (20001-point table) and the colorbar range from the tick labels.
Grid (from the cell edges): alpha = 45, 43.75, ..., 6.25 deg (32 rows);
log10 R = 1 + k log10(1.25), k = 0..30, then 4.0, 4.125, ..., 5.0 (40 columns).
Resolution: viridis has 256 colours, so (a) is quantised in steps of 0.214 in B (+-0.11) and (b) in steps of 0.38 per cent.
Checks: on the contour lines of panel (a) (B = 4, 5, ..., 20) the grid gives the contour level within 0.05;
(a)/B_max exceeds (b) by 1-6 per cent (more at small alpha), within the paper's own figure.
OUT.npz: logR (40), alpha (32), B (32 x 40, panel a), frac (32 x 40, panel b, per cent).
"""
import sys
import numpy as np
import pymupdf as fitz
from matplotlib import colormaps

page = fitz.open(sys.argv[1])[6]
lut = colormaps["viridis"](np.linspace(0, 1, 20001))[:, :3]
s = np.r_[1 + np.log10(1.25) * np.arange(31), 4 + 0.125 * np.arange(9)]
edges = (s[1:] + s[:-1]) / 2
alg = 45 - 1.25 * np.arange(32)
al = lambda y: 10 + (265.55 - y) / (265.55 - 105.85) * 35       # y of tick labels "10" and "45"
res = {}
#        axis x-range (= colorbar), x of the first and last colorbar tick labels and their values
PANELS = {"a": (90.555, 294.151, 117.85, 266.8, 10, 50), "b": (310.61, 514.21, 325.3, 494.5, 10, 90)}
for pan, (X0, X1, xt1, xt9, t1, t9) in PANELS.items():
    vmin = t1 + (X0 - xt1) * (t9 - t1) / (xt9 - xt1)
    vmax = t1 + (X1 - xt1) * (t9 - t1) / (xt9 - xt1)
    G = np.full((32, 40), np.nan)
    miss = 0
    for g in page.get_drawings():
        r = g["rect"]
        if not (g.get("fill") and g["type"] == "f" and 95 < r.y0 < 290 and r.width < 10 and X0 - 8 < r.x0 < X1):
            continue
        dx = 1 + 4 * (r.x0 - X0) / (X1 - X0)
        k = 0 if dx < edges[0] - 0.03 else int(np.argmin(abs(edges - dx))) + 1
        a = 0.5 * (al(r.y0) + al(r.y1))
        m = int(np.argmin(abs(alg - a)))
        assert abs(alg[m] - a) < 0.1, a
        e = ((lut - np.array(g["fill"])) ** 2).sum(1)
        j = int(e.argmin())
        miss = max(miss, float(np.sqrt(e[j])))
        G[m, k] = vmin + j / 20000 * (vmax - vmin)
    print(f"panel {pan}: colorbar {vmin:.3f}-{vmax:.3f}, filled {np.isfinite(G).sum()}/{G.size}, max colour miss {miss:.4f}")
    res[pan] = G
np.savez_compressed(sys.argv[2], logR=s, alpha=alg, B=res["a"], frac=res["b"])
