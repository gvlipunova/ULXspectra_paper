#!/usr/bin/env python3
"""Schematic of the accretion-rate profiles (fig:mdot_profiles; layout: the author's sketch 2026-11-21).

Main model, Eq. (mdot_setin): mdot/mdot_0 linear in x = r/R_in from f_in at x = 1 to 1 at x_sph = R_sph/R_in (solid);
SS73, Eq. (mdot_SS73): mdot/mdot_0 = r/R_sph, which is 1/mdot_0 at R_in = 6 R_g with R_sph = 6 mdot_0 R_g (dashed).
Constant mdot_0 beyond R_sph. Log axes. Illustrative values: mdot_0 = 100 (so x_sph = 100 for r_in,f = 6), f_in = 0.3.

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
MDOT0, FIN = 100.0, 0.3
XSP = MDOT0                      # SS73 with r_in,f = 6: R_sph/R_in = 6 mdot_0 R_g / (6 R_g)
x = np.logspace(0, np.log10(XSP), 300)
main = FIN + (1 - FIN) * (x - 1) / (XSP - 1)
ss73 = x / XSP

fig, ax = plt.subplots(figsize=(3.3, 2.6))
ax.plot(x, main, color="k", lw=1.5, label="main model")
ax.plot(x, ss73, color="k", lw=1.2, ls="--", label="SS73")
xo = np.array([XSP, XSP * 6])
ax.plot(xo, [1, 1], color="k", lw=1.5)
for y in (1, FIN, 1 / MDOT0):                       # guides to the y axis
    xe = XSP if y == 1 else 1
    ax.plot([0.8, xe], [y, y], color="0.6", lw=0.7, ls=":")
ax.plot([XSP, XSP], [0.006, 1], color="0.6", lw=0.7, ls=":")
ax.plot([1, 1], [0.006, 1 / MDOT0], color="0.6", lw=0.7, ls=":")
ax.plot([1, 1, XSP], [FIN, 1 / MDOT0, 1], "o", color="k", ms=3)
ax.text(8, 0.06, "SS73", fontsize=8, rotation=30)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(0.8, XSP * 6); ax.set_ylim(0.006, 2)
ax.set_xticks([1, XSP]); ax.set_xticklabels(["1", r"$R_{\rm sph}/R_{\rm in}$"])
ax.set_yticks([1 / MDOT0, FIN, 1]); ax.set_yticklabels([r"$1/\dot m_0$", r"$f_{\rm in}$", "1"])
ax.minorticks_off()
ax.set_xlabel(r"$x = r/R_{\rm in} = r/(R_{\rm g}\,r_{\rm in,f})$")
ax.set_ylabel(r"$\dot M/\dot M_0 = \dot m/\dot m_0$")
ax.legend(loc="lower right", frameon=False)
fig.savefig(OUT, bbox_inches="tight")
print(OUT)
