"""Reduced chi2 of the best fit of every preset for each source (fig:chi2_all; the author's request
2026-11-19: version of fig:chi2_overview without the notes, with all BH and all NS presets).

Final round (second version of the paper, 2026-11-28): the fit that stands for each preset
(column "selected" of ULXspectra-mc summaries/final_round_all_fits.tsv, 9fc8e3c; final_round_data.py).
Rows: the sources of tab:sources, in its order, NGC247SS twice (0.3-10 keV and 0.3-1.7 keV); background: type
in tab:sources (BH candidate grey, NS or NS candidate orange, accretor unknown no background). Squares: one
per preset, the 5 BH presets black, the 8 NS presets orange, semi-transparent so that overlaps show. Open
square: NGC247SS NS5ar (0.3-10 keV), which fails the Monte Carlo check (Notes 15-16). NGC247S BH4a passes
it in the final round (Note 18) and is no longer marked.

    python3 figures/plot_chi2_all.py [ULXspectra-mc] [OUT.pdf]
Data: ULXspectra-mc summaries (branch mc-transfer-corrections, 9fc8e3c).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import final_round_data as frd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "legend.fontsize": 8})  # sized for the page (text 10 pt)
from matplotlib.patches import Rectangle

B = sys.argv[1] if len(sys.argv) > 1 else "/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra-mc"
OUT = sys.argv[2] if len(sys.argv) > 2 else "figures/chi2_all.pdf"

ORANGE, GREY = "#e07b1a", "0.55"
FITS, _ = frd.load(B)
vals = [float(r["red_chi2"]) for r in FITS.values()]
X0, XN = min(vals) / 2, max(vals) * 2

n = len(frd.ROWS)
fig, ax = plt.subplots(figsize=(3.3, 0.36 * n + 1.3))
for k, (lab, src, band, typ) in enumerate(frd.ROWS):
    y = n - 1 - k
    if typ:                               # no background: accretor unknown
        ax.add_patch(Rectangle((X0, y - 0.4), XN - X0, 0.8, color=ORANGE if typ == "NS" else GREY, alpha=0.18, lw=0))
    for (s_, b_, _), r in FITS.items():
        if (s_, b_) != (src, band):
            continue
        is_ns = r["preset"].startswith("NS")
        c = ORANGE if is_ns else "k"
        yy = y + (-0.15 if is_ns else 0.15)   # BH above, NS below the row centre
        if (src, band, r["preset"]) in frd.FAILS_MC:
            ax.plot(float(r["red_chi2"]), yy, "s", ms=5, mfc="none", mec=c, mew=1.0)
        else:
            ax.plot(float(r["red_chi2"]), yy, "s", ms=5, mfc=c, mec="k", mew=0.4, alpha=0.55)
ax.set_xscale("log"); ax.set_xlim(X0, XN); ax.set_ylim(-0.6, n - 0.4)
ax.set_yticks(range(n)); ax.set_yticklabels([r[0] for r in frd.ROWS][::-1])
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("normalized reduced $\\chi^2$ of the best fit\n($\\sigma = 0.08$ dex)")
ax.plot([], [], "s", mfc="k", mec="k", alpha=0.55, label="BH presets (5)")
ax.plot([], [], "s", mfc=ORANGE, mec="k", alpha=0.55, label="NS presets (8)")
ax.plot([], [], "s", mfc="none", mec="k", label="fails the MC check")
ax.add_patch(Rectangle((0, 0), 0, 0, color=GREY, alpha=0.3, label="BH candidate"))
ax.add_patch(Rectangle((0, 0), 0, 0, color=ORANGE, alpha=0.3, label="NS or NS candidate"))
ax.add_patch(Rectangle((0, 0), 0, 0, facecolor="white", edgecolor="0.6", lw=0.6, label="accretor unknown"))
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=7.5, frameon=False)
fig.savefig(OUT, bbox_inches="tight")
print(OUT)
