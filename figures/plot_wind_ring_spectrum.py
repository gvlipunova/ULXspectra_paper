#!/usr/bin/env python3
"""Spectrum of one wind ring (fig:wind_ring_spectrum; layout: the author's sketch 2026-11-24). Illustrates Eqs. (fcor), (Inu_wind):

  I_nu = f_cor B_nu(T_w,raw)            the diluted blackbody of the ring (solid, hatched)
  B_nu(T_w,raw)                         the blackbody at the colour temperature (dashed)
  int I_nu dnu = f_cor sigma T_w,raw^4/pi = sigma T_w^4/pi, T_w = f_cor^(1/4) T_w,raw (Eq. fcor); B_nu(T_w) not drawn (author 2026-11-24)

Both B_nu(T_w,raw) and I_nu peak at nu_max = 2.821 k T_w,raw / h.
Illustrative values: k T_w,raw = 0.1 keV, f_cor = 0.51 (f_cor^(1/4) = 0.846, the NGC5408 BH3a fit of fig:temperatures,
ULXspectra-mc for_paper_session.md Note 5). Computed from the formulas, not from the code.

    python3 figures/plot_wind_ring_spectrum.py [OUT.pdf]
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 9, "ytick.labelsize": 9,
                     "legend.fontsize": 8})  # sized for the page (text 10 pt)

OUT = sys.argv[1] if len(sys.argv) > 1 else "figures/wind_ring_spectrum.pdf"
H, K, C = 6.62607e-27, 1.380649e-16, 2.99792458e10
KEV = 1.602177e-9 / K                      # K per keV
T_RAW = 0.1 * KEV
FCOR = 0.51
T_W = FCOR ** 0.25 * T_RAW


def bnu(nu, T):
    return 2 * H * nu ** 3 / C ** 2 / np.expm1(H * nu / (K * T))


nu = np.logspace(14.7, 17.6, 600)
b_raw = bnu(nu, T_RAW)
i_nu = FCOR * b_raw
NUMAX = 2.821 * K * T_RAW / H

fig, ax = plt.subplots(figsize=(3.2, 2.7))
ax.fill_between(nu, 1e-30, i_nu, facecolor="none", edgecolor="#c0392b", hatch="////", lw=0)
ax.loglog(nu, b_raw, color="#2a9d55", lw=1.4, ls="--", label=r"$B_\nu(T_{\rm w,raw})$")
ax.loglog(nu, i_nu, color="#c0392b", lw=1.6, label=r"$I_\nu = f_{\rm cor} B_\nu(T_{\rm w,raw})$")
ymax = b_raw.max()
ax.set_ylim(ymax * 1e-4, ymax * 6)
ax.set_xlim(nu[0], nu[-1])
ax.axvline(NUMAX, color="0.5", lw=0.7, ls=(0, (4, 3)))
ax.text(NUMAX * 1.1, ymax * 2.2, r"$\nu_{\max}$", fontsize=8, ha="left", va="center")
ax.text(1.5e16, ymax * 4e-4, r"$\int I_\nu\,{\rm d}\nu = f_{\rm cor}\,\sigma T_{\rm w,raw}^4/\pi$", fontsize=8,
        ha="center", bbox=dict(fc="white", ec="none", pad=1))
ax.set_xlabel(r"$\nu$ (Hz)")
ax.set_ylabel(r"$I_\nu$ (erg cm$^{-2}$ s$^{-1}$ Hz$^{-1}$ sr$^{-1}$)")
ax.legend(loc="upper left", frameon=False, handlelength=2.2)
fig.savefig(OUT, bbox_inches="tight")
print(OUT, f"nu_max = {NUMAX:.3g} Hz, T_w/T_raw = {FCOR ** 0.25:.3f}, RJ ratio = {FCOR ** 0.75:.3f}")
