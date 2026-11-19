"""Reduced chi2 of the best fit of every preset for each source (fig:chi2_all; the author's request
2026-11-19: version of fig:chi2_overview without the notes, with all BH and all NS presets).

Rows: the sources of tab:sources, in its order; background: type in tab:sources (BH candidate grey,
NS or NS candidate orange). Squares: one per preset, fits with the transfer correction, 0.3-10 keV
(run tag mc_0p3-10keV, summaries/refits_summary.tsv): the 5 BH presets black, the 8 NS presets orange,
semi-transparent so that overlaps show. Open square: NGC247S BH4a, which fails the Monte Carlo check.

    python3 figures/plot_chi2_all.py [ULXspectra-mc] [OUT.pdf]
Data: ULXspectra-mc summaries (branch mc-transfer-corrections, e597ba3).
"""
import csv, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

B = sys.argv[1] if len(sys.argv) > 1 else "/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra-mc"
OUT = sys.argv[2] if len(sys.argv) > 2 else "figures/chi2_all.pdf"

# Type column of tab:sources (sections/09_fitting.tex): True = NS (PULX or NS candidate)
SOURCES = [("HolmII", False), ("HolmIX", False), ("M101ULS", False), ("M51ULS", True), ("M81ULS", True),
           ("NGC1313B", False), ("NGC1313H", True), ("NGC247S", True), ("NGC247SS", True), ("NGC300", True),
           ("NGC5408", False), ("NGC55", False), ("NGC6946", False), ("NGC7793", True)]
ORANGE, GREY = "#e07b1a", "0.55"
FAILS_MC = {("NGC247S", "BH4a")}

rows = [r for r in csv.DictReader(open(B + "/summaries/refits_summary.tsv"), delimiter="\t")
        if r["run_dir"].endswith(".mc_0p3-10keV")]
vals = [float(r["red_chi2"]) for r in rows]
X0, XN = min(vals) / 2, max(vals) * 2

n = len(SOURCES)
fig, ax = plt.subplots(figsize=(6.5, 0.42 * n + 1.0))
for k, (src, ns) in enumerate(SOURCES):
    y = n - 1 - k
    ax.add_patch(Rectangle((X0, y - 0.4), XN - X0, 0.8, color=ORANGE if ns else GREY, alpha=0.18, lw=0))
    for r in rows:
        if r["source"] != src:
            continue
        is_ns = r["preset"].startswith("NS")
        c = ORANGE if is_ns else "k"
        yy = y + (-0.15 if is_ns else 0.15)   # BH above, NS below the row centre
        if (src, r["preset"]) in FAILS_MC:
            ax.plot(float(r["red_chi2"]), yy, "s", ms=7, mfc="none", mec=c, mew=1.0)
        else:
            ax.plot(float(r["red_chi2"]), yy, "s", ms=7, mfc=c, mec="k", mew=0.4, alpha=0.55)
ax.set_xscale("log"); ax.set_xlim(X0, XN); ax.set_ylim(-0.6, n - 0.4)
ax.set_yticks(range(n)); ax.set_yticklabels([s for s, _ in SOURCES][::-1])
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel(r"normalized reduced $\chi^2$ of the best fit ($\sigma = 0.08$ dex)")
ax.plot([], [], "s", mfc="k", mec="k", alpha=0.55, label="BH presets (5)")
ax.plot([], [], "s", mfc=ORANGE, mec="k", alpha=0.55, label="NS presets (8)")
ax.plot([], [], "s", mfc="none", mec="k", label="fails the MC check")
ax.add_patch(Rectangle((0, 0), 0, 0, color=GREY, alpha=0.3, label="BH candidate (Table 5)"))
ax.add_patch(Rectangle((0, 0), 0, 0, color=ORANGE, alpha=0.3, label="NS or NS candidate (Table 5)"))
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=7.5, frameon=False)
fig.savefig(OUT, bbox_inches="tight")
print(OUT)
