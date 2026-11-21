#!/usr/bin/env python3
"""Radial profiles of the viscous torque and of the disc temperature for a BH (fig:torque, fig:temperature;
author's request 2026-11-21). Computed from the equations of Sect. 4, not from the code:

  F_vis(r) = F_in + int_{h(R_in)}^{h(r)} Mdot dh,  h = sqrt(GM r), F_in = 0 (BH)            Eq. (Fvis)
  Q_vis = 3/(8 pi) F_vis Omega_K / r^2                                                      Eq. (Qvis)
  sigma T_vis^4 = Q_vis (r > R_trap),  Q_vis(R_trap) (R_trap/r)^2 (R_in <= r <= R_trap)      Eq. (Teff)
  T_disc = (1 - eps_w)^(1/4) T_vis inside R_sph, T_vis outside                              Eq. (Tdisc)
  R_trap = 12 mdot_0 R_g (z/r = 0.5, eta_Edd = 1/12)                                        Eq. (rtrap)

Profiles: main model, Eq. (mdot_setin), with f_in; SS73, Eq. (mdot_SS73); a disc without wind (Mdot = Mdot_0).
Illustrative values as fig:mdot_profiles: mdot_0 = 50, r_in,f = 6, R_sph = 6 mdot_0 R_g (x_sph = 50), f_in = 0.3,
eps_w = 0.5; then x_trap = R_trap/R_in = 2 mdot_0 = 100. Units: GM = R_in = Mdot_0 = 1; F in Mdot_0 h(R_in),
T in T_vis of the disc without wind at its maximum.

    python3 figures/plot_torque_temperature.py [OUT_DIR]
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 9, "ytick.labelsize": 9,
                     "legend.fontsize": 8})  # sized for the page (text 10 pt)

OUT = sys.argv[1] if len(sys.argv) > 1 else "figures"
MDOT0, RINF, FIN, EPSW = 50.0, 6.0, 0.3, 0.5
XSP = 6 * MDOT0 / RINF                 # R_sph = 6 mdot_0 R_g
XTR = 12 * MDOT0 / RINF                # R_trap = 12 mdot_0 R_g
x = np.logspace(0, np.log10(3e3), 4000)
h = np.sqrt(x)                         # h/h(R_in)


def mdot(prof):
    if prof == "main":
        m = FIN + (1 - FIN) * (x - 1) / (XSP - 1)
    elif prof == "ss73":
        m = x / XSP
    else:
        m = np.ones_like(x)
    return np.where(x < XSP, m, 1.0) if prof != "nowind" else m


def torque(m):                         # F = int Mdot dh, trapezoid on the fine grid, F(R_in) = 0
    return np.concatenate([[0], np.cumsum(0.5 * (m[1:] + m[:-1]) * np.diff(h))])


def t_vis(F):
    Q = F * x ** -1.5 / x ** 2         # Q_vis up to a constant: F Omega_K / r^2, Omega_K = x^-3/2
    Qtr = np.interp(XTR, x, Q)
    s = np.where(x > XTR, Q, Qtr * (XTR / x) ** 2)
    return s ** 0.25


style = {"main": dict(color="k", lw=1.5, label="main model"),
         "ss73": dict(color="k", lw=1.2, ls="--", label="SS73"),
         "nowind": dict(color="0.55", lw=1.0, ls=":", label="no wind")}
F = {p: torque(mdot(p)) for p in style}
T = {p: t_vis(F[p]) for p in style}
T0 = T["nowind"].max()


def mark(ax):
    ax.set_xscale("log"); ax.set_xlim(1, x[-1])
    tr = ax.get_xaxis_transform()       # x in data, y in axes units: labels above the frame, apart
    ax.text(XSP / 1.25, 1.02, r"$R_{\rm sph}$", transform=tr, ha="right", va="bottom")
    ax.text(XTR * 1.25, 1.02, r"$R_{\rm trap}$", transform=tr, ha="left", va="bottom")
    for v in (XSP, XTR):
        ax.axvline(v, color="0.6", lw=0.7, ls=":")
    ax.set_xlabel(r"$x = r/R_{\rm in}$")


# NS: torque at R_in = R_m, F_in = beta_t Mdot(R_m) h(R_m), beta_t = 1 (Eq. Fin_NS); x = r/R_m. The normalized profiles
# depend only on x_sph and f_in, so x_sph = 50 stands e.g. for mdot_0 = 500, R_m = 60 R_g.
FNS = {p: F[p] + mdot(p)[0] for p in ("main", "nowind")}
fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.7), sharey=True)
for ax, FF, tag in ((axs[0], F, "(a) BH"), (axs[1], FNS, "(b) NS")):
    for p, st in style.items():
        if p in FF:
            ax.plot(x, FF[p], **st)
    ax.set_yscale("log"); ax.set_ylim(1e-2, 80)
    mark(ax)
    ax.text(20, 6, r"$\sim\dot M_0\sqrt{GMr}$", color="0.4", fontsize=8.5, ha="right")
    ax.text(0.04, 0.93, tag, transform=ax.transAxes, va="top")
    ax.legend(loc="lower right", frameon=False)
axs[0].set_ylabel(r"$F_{\rm vis}/[\dot M_0\,h(R_{\rm in})]$")
axs[1].set_xlabel(r"$x = r/R_{\rm m}$")
fig.savefig(f"{OUT}/torque_profile.pdf", bbox_inches="tight")

fig, ax = plt.subplots(figsize=(3.3, 2.7))
ax.plot(x, T["nowind"] / T0, **style["nowind"])
ax.plot(x, T["main"] / T0, color="k", lw=1.0, ls="-.", label=r"main model, $T_{\rm vis}$")
td = np.where(x < XSP, (1 - EPSW) ** 0.25, 1.0) * T["main"] / T0
ax.plot(x, td, color="k", lw=1.5, label=r"main model, $T_{\rm disc}$")
ax.set_yscale("log"); ax.set_ylim(0.01, 1.5)
mark(ax)
ax.set_ylabel(r"$T$ / max $T_{\rm vis}$ (no wind)")
ax.legend(loc="lower left", frameon=False)
fig.savefig(f"{OUT}/temperature_profile.pdf", bbox_inches="tight")
print("written", F["main"][np.searchsorted(x, XSP)], T["main"][0] / T0)
