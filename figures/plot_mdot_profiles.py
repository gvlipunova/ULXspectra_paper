#!/usr/bin/env python3
"""Schematic of the accretion-rate profiles (fig:mdot_profiles; layout: the author's sketch 2026-11-21).

Main model, Eq. (mdot_setin): mdot/mdot_0 linear in x = r/R_in from f_in at x = 1 to 1 at x_sph = R_sph/R_in (solid);
SS73, Eq. (mdot_SS73): mdot/mdot_0 = r/R_sph, which is 1/mdot_0 at R_in = 6 R_g with R_sph = 6 mdot_0 R_g (dashed).
Constant mdot_0 beyond R_sph. x logarithmic, y linear. Illustrative values: mdot_0 = 50 (so x_sph = 50 for r_in,f = 6), f_in = 0.3.

    python3 figures/plot_mdot_profiles.py [OUT.pdf]
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 9, "ytick.labelsize": 9,
                     "legend.fontsize": 8})  # sized for the page (text 10 pt)

OUT = sys.argv[1] if len(sys.argv) > 1 else "figures/mdot_profiles.pdf"
MDOT0, FIN = 50.0, 0.3
XSP = MDOT0                      # SS73 with r_in,f = 6: R_sph/R_in = 6 mdot_0 R_g / (6 R_g)
x = np.logspace(0, np.log10(XSP), 300)
main = FIN + (1 - FIN) * (x - 1) / (XSP - 1)
ss73 = x / XSP

fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.6), sharey=True)   # (a) BH, (b) NS (author 2026-11-21)
for ax, ns in ((axs[0], False), (axs[1], True)):
    ax.plot(x, main, color="k", lw=1.5, label="main model")
    if not ns:                                        # no SS73 in the NS panel
        ax.plot(x, ss73, color="k", lw=1.2, ls="--", label="SS73")
    ax.plot([XSP, XSP * 6], [1, 1], color="k", lw=1.5)
    ys = (1, FIN) if ns else (1, FIN, 1 / MDOT0)
    for y in ys:                                      # guides to the y axis
        ax.plot([0.8, XSP if y == 1 else 1], [y, y], color="0.6", lw=0.7, ls=":")
    ax.plot([XSP, XSP], [0, 1], color="0.6", lw=0.7, ls=":")
    pts_x, pts_y = ([1, XSP], [FIN, 1]) if ns else ([1, 1, XSP], [FIN, 1 / MDOT0, 1])
    if not ns:
        ax.plot([1, 1], [0, 1 / MDOT0], color="0.6", lw=0.7, ls=":")
    ax.plot(pts_x, pts_y, "o", color="k", ms=3)
    ax.set_xscale("log")                              # x logarithmic, y linear (author 2026-11-21)
    ax.set_xlim(0.8, XSP * 6); ax.set_ylim(0, 1.12)
    ax.set_xticks([1, 10, 100]); ax.set_xticklabels(["1", "10", "100"])
    ax.tick_params(which="minor", length=2)
    ax.grid(which="major", axis="x", color="0.85", lw=0.5)
    rin = r"R_{\rm m}" if ns else r"R_{\rm in}"
    top = ax.secondary_xaxis("top", functions=(lambda v: v, lambda v: v))
    top.set_xticks([XSP], [rf"$R_{{\rm sph}}/{rin}$"]); top.minorticks_off()
    ax.set_xlabel(rf"$x = r/{rin}$" if ns else r"$x = r/R_{\rm in} = r/(R_{\rm g}\,r_{\rm in,f})$")
    ax.text(0.04, 0.95, "(b) NS" if ns else "(a) BH", transform=ax.transAxes, va="top")
    ax.legend(loc="lower right", frameon=False)
# special values as axis labels, next to the axes (shared y)
axs[0].set_yticks([1 / MDOT0, FIN, 1]); axs[0].set_yticklabels([r"$1/\dot m_0$", r"$f_{\rm in}$", "1"])
axs[0].set_ylabel(r"$\dot M/\dot M_0 = \dot m/\dot m_0$")
fig.savefig(OUT, bbox_inches="tight")
print(OUT)
