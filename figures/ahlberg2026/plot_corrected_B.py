#!/usr/bin/env python3
"""B(i) of the model with and without the transfer correction against the Monte Carlo through the wind, for the
seven NGC 7793 parameter sets of App. C.7, paragraph "The corrected model" (fig:corrected_B; author's request 2026-11-20).

Usage:  python3 plot_corrected_B.py DATA_DIR FIG_DIR
Reads DATA_DIR/wind_mc.npz (made by run_all.sh: reduce_wind_mc.py; code commit 2272e8a); writes FIG_DIR/corrected_B_of_i.png.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9, "xtick.labelsize": 8.5,
                     "ytick.labelsize": 8.5, "legend.fontsize": 8})  # sized for the page (text 10 pt)

D, F = sys.argv[1], sys.argv[2]
W = np.load(f"{D}/wind_mc.npz")
labs = [str(x) for x in W["labels"]]
we = W["mu_edges"]; wc = np.degrees(np.arccos(0.5 * (we[1:] + we[:-1])))

fig, axs = plt.subplots(2, 4, figsize=(7.2, 4.2), sharex=True, sharey=True)
axs = axs.ravel()
for ax, lab in zip(axs, labs):
    tc = float(W[f"{lab}:theta_c"]); ii = np.degrees(np.arccos(W[f"{lab}:mu"]))
    ax.semilogy(ii, W[f"{lab}:B1"], color="#2f6bd6", lw=1.6)
    ax.semilogy(ii, W[f"{lab}:B0"], color="#e07b00", lw=1.0, ls="--")
    h = W[f"{lab}:mc_counts"]; n = W[f"{lab}:mc_in"][1]; ok = h > 0
    ax.errorbar(wc[ok], (h / n / np.diff(we))[ok], yerr=(np.sqrt(h) / n / np.diff(we))[ok], fmt="o", ms=2.5,
                color="k", elinewidth=0.6)
    ax.axvline(tc, color="0.5", lw=0.7, ls=":")
    preset, w = lab.split(",")
    ax.set_title(f"{preset}, ω = {w[2:]}, θ$_c$ = {tc:.0f}°", fontsize=8)
    ax.set(xlim=(0, 90), ylim=(0.01, 20))
    ax.grid(alpha=0.25)
for ax in axs[4:]:
    ax.set_xlabel("i [deg]")
for ax in axs[::4]:
    ax.set_ylabel("B(i)")
ax = axs[-1]
ax.axis("off")
ax.plot([], [], color="#2f6bd6", lw=1.6, label="model, with correction")
ax.plot([], [], color="#e07b00", lw=1.0, ls="--", label="model, without")
ax.errorbar([], [], yerr=[], fmt="o", ms=2.5, color="k", label="Monte Carlo")
ax.plot([], [], color="0.5", lw=0.7, ls=":", label="θ$_c$")
ax.legend(loc="center", frameon=False)
fig.tight_layout()
fig.savefig(f"{F}/corrected_B_of_i.png", dpi=190, bbox_inches="tight")
print(f"{F}/corrected_B_of_i.png")
