"""Mass from the fits against published masses (fig:masses; layout: the author's sketch 2026-11-19).

x: published range of M_X (tab:masses, sections/A5_masses.tex); y: 68% posterior interval of M of the best BH
fit of the source (set "BH" of summaries/best_refit_per_source.tsv, posterior_summary.txt in
summaries/best_refit_spectra/; NGC247S: BH3a). One rectangle per published estimate, labelled with the source
name (once per source; Table tab:masses lists the estimates). Limits: the rectangle runs to the edge of the plot, with a dashed outline. A single value (~5000 Msun) is drawn
+-5%. Sources with no published mass (NS, n.m.) are not shown.

    python3 figures/plot_mass_comparison.py [ULXspectra-mc] [OUT.pdf]
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
       ("NGC247S", 600, None, "lower", "Jin+11"), ("NGC247SS", 600, None, "lower", "Jin+11"),
       ("NGC5408", 1000, 9000, "range", "Strohmayer+09"), ("NGC5408", 800, None, "lower", "Dheeraj+12"),
       ("NGC5408", 207, 1851, "range", "Majumder+23, a=0"), ("NGC5408", 104, 635, "range", "Majumder+23, a=0.99"),
       ("NGC55", 6, 14, "range", "Barra+22"),
       ("NGC6946", 1000, 4000, "range", "Rao+10"), ("NGC6946", 248, 2221, "range", "Majumder+23, a=0"),
       ("NGC6946", 214, 696, "range", "Majumder+23, a=0.99"),
       ("NGC7793", None, 15, "upper", "Motch+14")]

best_bh = {}
for l in open(B + "/summaries/best_refit_per_source.tsv"):
    f = l.split("\t")
    if f[0] == "BH":
        best_bh[f[1]] = f"{B}/summaries/best_refit_spectra/{f[1]}.{f[2]}/posterior_summary.txt"
best_bh["NGC247S"] = ("/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra-refit/results/"
                      "mcmc_NGC247S.BH3a.mc_0p3-10keV/posterior_summary.txt")


def mass_interval(path):
    on = False
    for l in open(path):
        if "physical parameters" in l:
            on = True
        elif on and l.startswith("log_m_bh"):
            m, lo, hi = map(float, l.split()[1:4])
            return m - lo, m + hi
    raise KeyError(path)


srcs = sorted({p[0] for p in PUB}, key=[p[0] for p in PUB].index)
col = {s: plt.cm.tab10(i % 10) for i, s in enumerate(srcs)}
fig, ax = plt.subplots(figsize=(7, 6))
ys = []
labelled = set()
for src, lo, hi, kind, tag in PUB:
    y0, y1 = mass_interval(best_bh[src]); ys += [y0, y1]
    if kind == "value":
        lo, hi = lo * 0.95, hi * 1.05
    x0 = XMIN if kind == "upper" else lo
    x1 = XMAX if kind == "lower" else hi
    ls = "--" if kind in ("lower", "upper") else "-"
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=True, fc=col[src], alpha=0.15, lw=0))
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec=col[src], lw=1.2, ls=ls))
    if src not in labelled:   # one label per source, at its first estimate
        labelled.add(src)
        ax.text(x0 * 1.05, y1 * 1.04, src, fontsize=7, color=col[src], va="bottom")
ax.plot([XMIN, XMAX], [XMIN, XMAX], color="0.4", lw=0.8)
ax.text(4e3, 6e3, "1:1", fontsize=8, color="0.4")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(XMIN, XMAX); ax.set_ylim(min(ys) / 1.5, max(ys) * 3)
ax.set_xlabel(r"$M_{\rm X}$, published ($M_\odot$)")
ax.set_ylabel(r"$M$, best BH fit, 68% interval ($M_\odot$)")
fig.savefig(OUT, bbox_inches="tight")
print(OUT)
