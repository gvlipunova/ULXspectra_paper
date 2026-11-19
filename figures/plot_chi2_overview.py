"""Overview of the best BH and NS fits per source against the type of the source
(fig:chi2_overview; layout: the author's sketch, 2026-11-19).

Rows: the sources of tab:sources, in its order. Row background: the type in
tab:sources, BH candidate grey, NS (PULX or candidate) orange. Squares: reduced
chi2 of the best BH fit (black) and of the best NS fit (orange), sets "BH" and
"NS" of summaries/best_refit_per_source.tsv; for NGC247S the BH fit is BH3a
(refits_summary.tsv), not BH4a, which fails the Monte Carlo check. Note at the
right end: preset of the best fit of the source (tab:bestfit_params), its
best-fit M (BH) or R_m (NS) and inclination.

    python3 figures/plot_chi2_overview.py [ULXspectra-mc] [OUT.pdf]
Data: ULXspectra-mc summaries (branch mc-transfer-corrections, e597ba3).
"""
import csv, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

B = sys.argv[1] if len(sys.argv) > 1 else "/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra-mc"
OUT = sys.argv[2] if len(sys.argv) > 2 else "figures/chi2_overview.pdf"

# Type column of tab:sources (sections/09_fitting.tex): True = NS (PULX or NS candidate)
SOURCES = [("HolmII", False), ("HolmIX", False), ("M101ULS", False), ("M51ULS", True), ("M81ULS", True),
           ("NGC1313B", False), ("NGC1313H", True), ("NGC247S", True), ("NGC247SS", True), ("NGC300", True),
           ("NGC5408", False), ("NGC55", False), ("NGC6946", False), ("NGC7793", True)]
ORANGE, GREY = "#e07b1a", "0.55"

rows = list(csv.DictReader(open(B + "/summaries/best_refit_per_source.tsv"), delimiter="\t"))
summ = list(csv.DictReader(open(B + "/summaries/refits_summary.tsv"), delimiter="\t"))
pick = {(r["set"], r["source"]): r for r in rows}
bh3a = [r for r in summ if r["source"] == "NGC247S" and r["preset"] == "BH3a" and r["run_dir"].endswith(".mc_0p3-10keV")][0]
pick[("BH", "NGC247S")] = pick[("all", "NGC247S")] = bh3a


def params(r):
    return {k.strip(): float(v) for k, v in (kv.split("=") for kv in r["params"].split(";"))}


def note(r):
    p = params(r)
    if r["preset"].startswith("NS"):   # R_m/R_g = 4.5 * 10**log_wind_inner_launch_x (r presets, r_in_factor = 4.5)
        q = rf"$R_{{\rm m}} = 10^{{{p['log_wind_inner_launch_x'] + 0.65321:.1f}}}\,R_{{\rm g}}$"
    else:
        m = 10 ** p['log_m_bh']
        q = rf"$M = {m:.2g}\,M_\odot$" if m < 10 else rf"$M = {m:.0f}\,M_\odot$"
    return rf"{r['preset']}: {q}, $i = {p['incl_deg']:.0f}^\circ$"


n = len(SOURCES)
fig, ax = plt.subplots(figsize=(7.2, 0.42 * n + 1.0))
X0, X1, XN = 2e-3, 1e2, 3e3
for k, (src, ns) in enumerate(SOURCES):
    y = n - 1 - k
    ax.add_patch(Rectangle((X0, y - 0.4), XN - X0, 0.8, color=ORANGE if ns else GREY, alpha=0.18, lw=0))
    for st, c in (("BH", "k"), ("NS", ORANGE)):
        r = pick.get((st, src))
        if r:
            ax.plot(float(r["red_chi2"]), y, "s", ms=8, mfc=c, mec="k", mew=0.6)
    ax.text(X1 * 1.15, y, note(pick[("all", src)]), va="center", fontsize=7.5)
ax.set_xscale("log"); ax.set_xlim(X0, XN); ax.set_ylim(-0.6, n - 0.4)
ax.set_yticks(range(n)); ax.set_yticklabels([s for s, _ in SOURCES][::-1])
ax.set_xticks([1e-2, 1e-1, 1, 1e1, 1e2])
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel(r"reduced $\chi^2$ of the best fit ($\sigma = 0.08$ dex)")
ax.plot([], [], "s", mfc="k", mec="k", label="best BH fit")
ax.plot([], [], "s", mfc=ORANGE, mec="k", label="best NS fit")
ax.add_patch(Rectangle((0, 0), 0, 0, color=GREY, alpha=0.3, label="BH candidate (Table 5)"))
ax.add_patch(Rectangle((0, 0), 0, 0, color=ORANGE, alpha=0.3, label="NS or NS candidate (Table 5)"))
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=4, fontsize=7.5, frameon=False)
fig.savefig(OUT, bbox_inches="tight")
print(OUT)
