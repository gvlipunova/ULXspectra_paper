"""Overview of the best BH and NS fits per source against the type of the source
(fig:chi2_overview; layout: the author's sketch, 2026-11-19).

Rows: the sources of tab:sources, in its order. Row background: the type in
tab:sources, BH candidate grey, NS (PULX or candidate) orange. Squares: reduced
chi2 of the best BH fit (black) and of the best NS fit (orange), sets "BH" and
"NS" of summaries/best_refit_per_source.tsv; for NGC247S the BH fit is BH3a
(refits_summary.tsv), not BH4a, which fails the Monte Carlo check. Note at the
right end: preset of the best fit of the source (tab:bestfit_params), its
best-fit M (BH) or R_m (NS) and inclination, and the free parameter farthest
from its default value in the preset (ULX.conf.example), the distance measured
in units of the prior range (psrcs/config_loader.py, 4ca9834).

    python3 figures/plot_chi2_overview.py [ULXspectra-mc] [OUT.pdf]
Data: ULXspectra-mc summaries (branch mc-transfer-corrections, e597ba3); presets ULX.conf.example 454490d.
"""
import csv, sys, configparser
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


# Prior ranges of the free parameters (psrcs/config_loader.py, ULXspectra-mc 4ca9834)
PRIOR = {"log_m_bh": (0.0, 4.0), "log_mdot0": (-2.0, 5.0), "eps_w": (1e-4, 0.999), "beta_w": (0.05, 3.0),
         "incl_deg": (0.0, 88.0), "omega_frac": (0.1, 0.85), "r_in_factor": (1.0, 20.0),
         "log_r_out_factor": (2.0, 10.0), "log_wind_inner_launch_x": (0.0, 4.0),
         "user_mdot_in_fraction": (0.0, 1.0), "log_magn_eta": (-5.0, 0.0)}
LABEL = {"log_m_bh": r"\log M", "log_mdot0": r"\log\dot m_0", "eps_w": r"\epsilon_{\rm w}", "beta_w": r"\beta_{\rm w}",
         "incl_deg": "i", "omega_frac": r"\Omega_{\rm w}/4\pi", "r_in_factor": r"R_{\rm in}/R_{\rm g}",
         "log_r_out_factor": r"\log R_{\rm out}/R_{\rm g}", "log_wind_inner_launch_x": r"\log R_{\rm m}/R_{\rm g}",
         "user_mdot_in_fraction": r"\dot m_{\rm in}/\dot m_0", "log_magn_eta": r"\log\eta_{\rm magn}"}
# Defaults: the preset values of ULX.conf.example at ULXspectra-mc 454490d (log_mdot0 = 1, user_mdot_in_fraction = 0.5
# where free, as asked by the author 2026-11-19). For a free parameter this is the centre of the walkers' starting ball,
# not part of the prior.
CONF = configparser.ConfigParser(inline_comment_prefixes="#")
CONF.read(B + "/ULX.conf.example")


def farthest(preset, p):
    """Free parameter with the largest |best - default| / prior range; returns (name, best, default)."""
    sec = CONF[preset]
    free = [x.strip() for x in sec["free_params"].split(",")]
    d = {k: float(sec[k]) for k in free}
    k = max(free, key=lambda k: abs(p[k] - d[k]) / (PRIOR[k][1] - PRIOR[k][0]))
    v, v0 = p[k], d[k]
    if k == "log_wind_inner_launch_x":   # shown as log R_m/R_g = log 4.5 + log x
        v, v0 = v + 0.65321, v0 + 0.65321
    return k, v, v0


def params(r):
    return {k.strip(): float(v) for k, v in (kv.split("=") for kv in r["params"].split(";"))}


def note(r):
    p = params(r)
    if r["preset"].startswith("NS"):   # R_m/R_g = 4.5 * 10**log_wind_inner_launch_x (r presets, r_in_factor = 4.5)
        q = rf"$R_{{\rm m}} = 10^{{{p['log_wind_inner_launch_x'] + 0.65321:.1f}}}\,R_{{\rm g}}$"
    else:
        m = 10 ** p['log_m_bh']
        q = rf"$M = {m:.2g}\,M_\odot$" if m < 10 else rf"$M = {m:.0f}\,M_\odot$"
    k, v, v0 = farthest(r["preset"], p)
    fmt = (lambda x: f"{x:.0f}") if k == "incl_deg" else (lambda x: f"{x:.2g}")
    if k == "incl_deg":
        return rf"{r['preset']}: {q}, $i = {p['incl_deg']:.0f}^\circ$ (def. {v0:.0f}$^\circ$)"
    return rf"{r['preset']}: {q}, $i = {p['incl_deg']:.0f}^\circ$; ${LABEL[k]} = {fmt(v)}$ (def. {fmt(v0)})"


n = len(SOURCES)
fig, ax = plt.subplots(figsize=(8.4, 0.42 * n + 1.0))
X0, X1, XN = 2e-3, 1e2, 3e4
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
