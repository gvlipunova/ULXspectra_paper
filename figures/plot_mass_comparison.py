"""Mass from the fits against published masses (fig:masses; layout: the author's sketch 2026-11-19).

x: published range of M_X (tab:masses, sections/A5_masses.tex); y: 68% posterior interval of M of the best BH
fit of the source and band in the final round (column best_BH of ULXspectra-mc
summaries/final_round_best_per_source.tsv, 9fc8e3c; posterior_summary.txt of its run; final_round_data.py).
NGC247SS is drawn twice, for the 0.3-10 keV fit (BH4a) and the 0.3-1.7 keV fit (BH2), both against Jin+11. One rectangle per published estimate, labelled with the source
name (once per source; Table tab:masses lists the estimates). Limits: the rectangle runs to the edge of the plot, with a dashed outline. A single value (~5000 Msun) is drawn
+-5%. Sources with no published mass (NS, n.m.) are not shown.

    python3 figures/plot_mass_comparison.py [ULXspectra-mc] [OUT.pdf]
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
OUT = sys.argv[2] if len(sys.argv) > 2 else "figures/mass_comparison.pdf"
XMIN, XMAX = 2.0, 2e5

# Published estimates of tab:masses: (source, lo, hi, kind, tag); kind: range, lower, upper, value
PUB = [("HolmII", 16, 36, "range", "Barra+24"), ("HolmII", 16, 70, "range", "Fogantini+26"),
       ("HolmII", 25, None, "lower", "Cseh+14"),
       ("HolmIX", 4, 60, "range", "Gill+21"),            # M = Mhat/alpha, Mhat 4-10, 1/6 <= alpha < 1
       ("M101ULS", 20, 30, "range", "Liu+13"), ("M101ULS", 3.2e4, 4.3e4, "range", "Titarchuk+16"),
       ("NGC1313B", 5000, 5000, "value", "Pasham+15"), ("NGC1313B", 2524, 6811, "range", "Huang19"),
       ("NGC1313B", 275, 2283, "range", "Majumder+23, a=0"), ("NGC1313B", 92, 883, "range", "Majumder+23, a=0.99"),
       ("NGC247S", 600, None, "lower", "Jin+11"), ("NGC247SS", 600, None, "lower", "Jin+11"),   # 600-3000 for a = 0, face-on; larger otherwise
       ("NGC5408", 1000, 9000, "range", "Strohmayer+09"), ("NGC5408", 800, None, "lower", "Pasham+12"),
       ("NGC5408", 207, 1851, "range", "Majumder+23, a=0"), ("NGC5408", 104, 635, "range", "Majumder+23, a=0.99"),
       ("NGC55", 6, 14, "range", "Barra+22"),
       ("NGC6946", 1000, 4000, "range", "Rao+10"), ("NGC6946", 130, 1300, "range", "Rao+10, break"), ("NGC6946", 248, 2221, "range", "Majumder+23, a=0"),
       ("NGC6946", 214, 696, "range", "Majumder+23, a=0.99"),
       ("NGC7793", None, 15, "upper", "Motch+14")]

FITS, BEST = frd.load(B)


def mass_interval(src, band=frd.FULL):
    m, lo, hi = frd.posterior(FITS[(src, band, BEST[(src, band)]["best_BH"])], "log_m_bh")   # linear M
    return m - lo, m + hi


# NGC247SS a second time, for the fit below 1.7 keV
PUB = PUB + [("NGC247SS, <1.7 keV", 600, None, "lower", "Jin+11")]
BAND = {"NGC247SS, <1.7 keV": ("NGC247SS", frd.SOFT)}

srcs = sorted({p[0] for p in PUB}, key=[p[0] for p in PUB].index)
col = {s: plt.cm.tab10(i % 10) for i, s in enumerate(srcs)}
fig, ax = plt.subplots(figsize=(3.4, 3.3))
ys = []
labelled = set()
for src, lo, hi, kind, tag in PUB:
    y0, y1 = mass_interval(*BAND.get(src, (src,))); ys += [y0, y1]
    if kind == "value":
        lo, hi = lo * 0.95, hi * 1.05
    x0 = XMIN if kind == "upper" else lo
    x1 = XMAX if kind == "lower" else hi
    ls = "--" if kind in ("lower", "upper") else "-"
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=True, fc=col[src], alpha=0.15, lw=0))
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec=col[src], lw=1.2, ls=ls))
    if src not in labelled:   # one label per source, at its first estimate
        labelled.add(src)
        if src in BAND:   # second NGC247SS rectangle: label below it, so that it does not cover the first one
            ax.text(XMAX / 1.1, y0 / 1.04, src, fontsize=7, color=col[src], va="top", ha="right")
        else:
            ax.text(x0 * 1.05, y1 * 1.04, src, fontsize=7, color=col[src], va="bottom")
ax.plot([XMIN, XMAX], [XMIN, XMAX], color="0.4", lw=0.8)
ax.text(30, 50, "1:1", fontsize=8, color="0.4", rotation=38)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(XMIN, XMAX); ax.set_ylim(min(ys) / 1.5, max(ys) * 3)
ax.set_xlabel(r"$M_{\rm X}$, published ($M_\odot$)")
ax.set_ylabel(r"$M$, best BH fit, 68% interval ($M_\odot$)")
fig.savefig(OUT, bbox_inches="tight")
print(OUT)
