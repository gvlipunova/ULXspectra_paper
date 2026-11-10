#!/usr/bin/env python3
"""Recover the boost-factor curves B(i) of Fig. 2, columns (a) and (b), of Ahlberg et al. 2026
(arXiv:2610.23089v1) from the vector graphics of the PDF.

Usage:  python3 extract_fig2.py 2610.23089v1.pdf ROW OUT.npz      ROW = L (top row) or Ch (middle row)

Fig. 2a: alpha = 5, 10, 15, 20, 25 deg at R = 1e3; Fig. 2b: alpha = 25 deg at R = 1e1 ... 1e5 (the alpha = 10 deg
curves of Fig. 2b are not extracted). Their B(i) is tallied in 500 inclination bins of equal solid angle
(their Sect. 3.1), so the curves are step functions in mu with steps of 0.002.
Each curve is stored as an (n, 2) array of (i [deg], B) under the key "a:alpha=<deg>" or "b:R=1e<k>".
Axis calibration: centres of the tick labels "0" and "80" (x) and "10" and "0.01" (y, log).
Check: integral of B over mu from 0 to 1 is 0.93-0.99 for the extracted curves (it is 1 by definition).
"""
import sys
import numpy as np
import pymupdf as fitz

pdf, row, out = sys.argv[1], sys.argv[2], sys.argv[3]
page = fitz.open(pdf)[3]
XC = {"a": (104.4, 214.5), "b": (241.7, 352.4)}              # x of tick labels "0" and "80"
Y10, Y001, YLO, YHI = {"Ch": (264.4, 337.6, 240, 345), "L": (142.2, 215.9, 118, 222)}[row]
KEY = {
    "a": {(0.267, 0.005, 0.329): "alpha=5", (0.254, 0.265, 0.53): "alpha=10", (0.164, 0.471, 0.558): "alpha=15",
          (0.135, 0.659, 0.518): "alpha=20", (0.478, 0.821, 0.318): "alpha=25"},
    "b": {(0.098, 0.098, 0.439): "R=1e1", (0.049, 0.049, 0.72): "R=1e2", (0.0, 0.0, 1.0): "R=1e3",
          (0.0, 0.402, 0.902): "R=1e4", (0.0, 0.804, 0.804): "R=1e5"},
}
res = {}
for pan, (x0, x80) in XC.items():
    for g in page.get_drawings():
        if g["type"] != "s" or len(g["items"]) < 20:
            continue
        c = tuple(round(x, 3) for x in g["color"])
        r = g["rect"]
        if c not in KEY[pan] or not (x0 - 5 < r.x0 < x0 + 5 and r.x1 < x80 + 20 and YLO < r.y0 < YHI):
            continue
        P = np.array([(q.x, q.y) for it in g["items"] for q in it[1:] if hasattr(q, "x")])
        i = (P[:, 0] - x0) * 80 / (x80 - x0)
        B = 10 ** (1 - 3 * (P[:, 1] - Y10) / (Y001 - Y10))
        o = np.argsort(i, kind="stable")
        res[f"{pan}:{KEY[pan][c]}"] = np.c_[i[o], B[o]]
for k, v in res.items():
    mu = np.cos(np.radians(np.clip(v[:, 0], 0, 90)))
    print(f"{row} {k:12s} points {len(v):5d}  int B dmu = {-np.trapezoid(v[:, 1], mu):.3f}")
np.savez_compressed(out, **res)
