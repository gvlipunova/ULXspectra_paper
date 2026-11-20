#!/usr/bin/env python3
"""Plain-text export of the results of Ahlberg et al. 2026 (arXiv:2610.23089v1) read from their figures
(data/ahlberg_fig2_L.npz, ahlberg_fig2_Ch.npz, ahlberg_fig4.npz; see README.md), for the calculation session
(Fig. 8 of App. C.7, opaque cone vs wind cone). Writes data/export/*.tsv and data/export/README.txt.

    python3 export_tables.py DATA_DIR
"""
import os, sys
import numpy as np

D = sys.argv[1]; O = f"{D}/export"; os.makedirs(O, exist_ok=True)
L, Ch, G = (np.load(f"{D}/{f}") for f in ("ahlberg_fig2_L.npz", "ahlberg_fig2_Ch.npz", "ahlberg_fig4.npz"))
mu_e = np.linspace(0, 1, 501)                      # their 500 bins of equal solid angle, d mu = 0.002
ic = np.degrees(np.arccos(0.5 * (mu_e[1:] + mu_e[:-1])))
ei = np.degrees(np.arccos(mu_e))


def bins500(F2, k):
    """As theirs500() in plot_ahlberg_comparison.py: B of the horizontal step between two bin edges."""
    i, B = F2[k].T
    out = np.full(500, np.nan)
    for b in range(500):
        lo, hi = ei[b + 1], ei[b]
        Bl = B[np.abs(i - lo) < 0.06]; Bh = B[np.abs(i - hi) < 0.06]
        common = [x for x in Bl if np.any(np.abs(Bh / x - 1) < 0.003)]
        if common:
            out[b] = np.median(common)
        else:
            inside = B[(i > lo + 0.06) & (i < hi - 0.06)]
            o_ = np.argsort(i)
            out[b] = np.median(inside) if inside.size else np.interp(ic[b], i[o_], B[o_])
    out[ic > i.max() + 0.5] = np.nan                # beyond the end of the drawn curve (B < 0.01, edge of the plot)
    return out


cols, data = [], []
for tag, F2 in (("L", L), ("Ch", Ch)):
    for k in F2.files:
        panel, par = k.split(":")
        name = {"a": "fig2a", "b": "fig2b", "b10": "fig2b_alpha10"}[panel]
        cols.append(f"B_{tag}_{name}_{par.replace('alpha=', 'alpha').replace('R=', 'R')}")
        data.append(bins500(F2, k))
data = np.array(data)
hdr = "# Ahlberg+2026 figure 2, B(i) read from the vector paths, in their 500 bins of equal solid angle.\n" \
      "# L: Lambertian walls (top row), Ch: electron-scattering (Chandrasekhar) walls (middle row).\n" \
      "# fig2a: alpha = 5-25 deg at R = 1e3; fig2b: alpha = 25 deg at R = 1e1-1e5; fig2b_alpha10: alpha = 10 deg at R = 1e1-1e5.\n" \
      "# NaN: below B = 0.01 (not drawn).\n"
with open(f"{O}/ahlberg_fig2_B_500bins.tsv", "w") as f:
    f.write(hdr + "mu_lo\tmu_hi\ti_center_deg\t" + "\t".join(cols) + "\n")
    for b in range(500):
        f.write(f"{mu_e[b]:.3f}\t{mu_e[b + 1]:.3f}\t{ic[b]:.3f}\t" + "\t".join(f"{v:.4g}" for v in data[:, b]) + "\n")
# requested by the author 2026-11-20: alpha = 10 and 25 deg, R = 1e2, 1e3, 1e4, i <= 20 deg, their 500 bins
want = [f"B_{t}_{p}_R1e{k}" for t in ("L", "Ch") for p in ("fig2b_alpha10", "fig2b") for k in (2, 3, 4)]
idx = [cols.index(c) for c in want]; sel = np.where(ic <= 20.5)[0][::-1]
with open(f"{O}/ahlberg_fig2b_alpha10_25_i0-20.tsv", "w") as f:
    f.write("# Ahlberg+2026 figure 2b, B(i) at i <= 20 deg in their bins of equal solid angle (d mu = 0.002), read from\n"
            "# the vector paths. Columns: walls (L Lambertian, Ch electron scattering), alpha (fig2b_alpha10 = 10 deg,\n"
            "# fig2b = 25 deg), R. Rows from the axis outwards.\n")
    f.write("mu_lo\tmu_hi\ti_center_deg\t" + "\t".join(c.replace("fig2b_R", "fig2b_alpha25_R") for c in want) + "\n")
    for b in sel:
        f.write(f"{mu_e[b]:.3f}\t{mu_e[b + 1]:.3f}\t{ic[b]:.3f}\t" + "\t".join(f"{data[j, b]:.4g}" for j in idx) + "\n")
mu20 = np.linspace(0, 1, 21)
with open(f"{O}/ahlberg_fig2_B_20bins.tsv", "w") as f:
    f.write(hdr.replace("in their 500 bins of equal solid angle", "averaged into 20 equal bins in mu (25 of their bins each)")
            + "# NaN if any of the 25 bins is not drawn.\n")
    f.write("mu_lo\tmu_hi\ti_center_deg\t" + "\t".join(cols) + "\n")
    for b in range(20):
        sl = slice(25 * b, 25 * b + 25)
        v = data[:, sl].mean(axis=1)
        f.write(f"{mu20[b]:.2f}\t{mu20[b + 1]:.2f}\t{np.degrees(np.arccos(0.5 * (mu20[b] + mu20[b + 1]))):.2f}\t"
                + "\t".join(f"{x:.4g}" for x in v) + "\n")
with open(f"{O}/ahlberg_fig4_mean_boost.tsv", "w") as f:
    f.write("# Ahlberg+2026 figure 4: mean boost at i <= alpha, electron-scattering walls, read from the cell colours.\n"
            "# B_mean: panel (a), resolution +-0.11; B_over_Bmax_pct: panel (b), resolution +-0.2 per cent;\n"
            "# panel (a)/B_max exceeds panel (b) by 1-6 per cent within their paper. Bmax = 1/(1 - cos alpha).\n")
    f.write("alpha_deg\tlog10R\tR\tB_mean\tB_over_Bmax_pct\tBmax\n")
    for a_i, a in enumerate(G["alpha"]):
        for r_i, lr in enumerate(G["logR"]):
            f.write(f"{a:.4g}\t{lr:.4f}\t{10 ** lr:.4g}\t{G['B'][a_i, r_i]:.4g}\t{G['frac'][a_i, r_i]:.4g}\t"
                    f"{1 / (1 - np.cos(np.radians(a))):.4g}\n")
open(f"{O}/README.txt", "w").write("""Results of Ahlberg et al. 2026 (arXiv:2610.23089v1) read from the vector paths of their figures
(paper repository, figures/ahlberg2026/; extraction checks in figures/ahlberg2026/README.md).

ahlberg_fig2_B_500bins.tsv  B(i) of their figure 2 in their 500 bins of equal solid angle (d mu = 0.002).
                            Lambertian (L) and electron-scattering (Ch) walls; alpha = 5, 10, 15, 20, 25 deg at R = 1e3
                            (fig2a), alpha = 25 deg at R = 1e1-1e5 (fig2b) and alpha = 10 deg at R = 1e1-1e5
                            (fig2b_alpha10, added 2026-11-20). NaN: below B = 0.01.
                            In all ten Lambertian curves our cone MC matches best when shifted by one bin towards the
                            axis (App. C.7, footnote); no shift is applied here.
ahlberg_fig2b_alpha10_25_i0-20.tsv  alpha = 10 and 25 deg, R = 1e2, 1e3, 1e4, i <= 20 deg (their 500-bin steps).
                            Check: fig2b alpha = 10, R = 1e3 equals fig2a alpha = 10 to median 0.7%.
ahlberg_fig2_B_20bins.tsv   the same averaged into 20 equal bins in mu (as Fig. 8 of the paper).
ahlberg_fig4_mean_boost.tsv mean boost at i <= alpha on their grid, alpha = 6.25-45 deg (32 values), R = 10-1e5 (40 values),
                            electron-scattering walls only.

Overlap with Fig. 8 (alpha = 45.6, 31.8, 25 deg; R = 1e2, 1e3, 1e4):
  B(i) curves: alpha = 25 deg and 10 deg, R = 1e2, 1e3, 1e4 (fig2b; L and Ch). No B(i) at 31.8 or 45.6 deg.
  Mean boost: alpha = 45 deg and 31.25 deg (nearest grid values) at R ~ 1e2, 1e3, 1e4; electron-scattering walls,
  0.94-0.96 of it for Lambertian walls (their figure 2a).
Reading error: steps of figure 2 are exact path coordinates; figure 4 +-0.11 in B.
""")
print(O, sorted(os.listdir(O)))
