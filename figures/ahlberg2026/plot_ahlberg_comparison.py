#!/usr/bin/env python3
"""Figures and numbers of the comparison with the published results of Ahlberg et al. 2026 (arXiv:2610.23089v1).

Usage:  python3 plot_ahlberg_comparison.py DATA_DIR FIG_DIR

Reads DATA_DIR/{ahlberg_fig2_L.npz, ahlberg_fig2_Ch.npz, ahlberg_fig4.npz, cone_mc_hist.npz, wind_mc.npz};
writes FIG_DIR/ahlberg_published_vs_cone_mc.png, FIG_DIR/ahlberg_published_vs_mc_transfer.png and
DATA_DIR/summary.txt (all numbers quoted in the text).
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
from matplotlib import colormaps

D, F = sys.argv[1], sys.argv[2]
L = np.load(f"{D}/ahlberg_fig2_L.npz")
Ch = np.load(f"{D}/ahlberg_fig2_Ch.npz")
G = np.load(f"{D}/ahlberg_fig4.npz")
C = np.load(f"{D}/cone_mc_hist.npz")
W = np.load(f"{D}/wind_mc.npz")
s, alg, GB = G["logR"], G["alpha"], G["B"]
mu_e = C["mu_edges"]; muc = 0.5 * (mu_e[1:] + mu_e[:-1]); ic500 = np.degrees(np.arccos(muc))
i_e_mu = C["i_edges_mu"]; icen = 89.5 - np.arange(90)                 # 1-deg bins, ascending in mu
out = []
P = lambda *a: out.append(" ".join(str(x) for x in a))
Bmax = lambda a: 1 / (1 - np.cos(np.radians(a)))
key = lambda a, lR: f"a{a:g}_logR{lR:.4f}"
fmt = mt.FuncFormatter(lambda v, _: f"{v:g}")


def theirs500(F2, k):
    """Value of their step curve in each of their 500 mu-bins: the B shared by the path points at the two
    bin edges (the horizontal segment); interpolation across the vertical steps would mix neighbouring bins."""
    i, B = F2[k].T
    ei = np.degrees(np.arccos(mu_e))                     # bin edges in i, descending
    out = np.full(ic500.size, np.nan)
    for b in range(ic500.size):
        lo, hi = ei[b + 1], ei[b]
        Bl = B[np.abs(i - lo) < 0.06]; Bh = B[np.abs(i - hi) < 0.06]
        common = [x for x in Bl if np.any(np.abs(Bh / x - 1) < 0.003)]
        if common:
            out[b] = np.median(common)
        else:                                            # no step at this edge pair: points inside the bin
            inside = B[(i > lo + 0.06) & (i < hi - 0.06)]
            out[b] = np.median(inside) if inside.size else np.interp(ic500[b], i, B)
    return out


def stairs_theirs(ax, F2, k, **kw):  # their curve as steps on their own 500 mu-bins
    ei = np.degrees(np.arccos(mu_e))
    ax.stairs(theirs500(F2, k)[::-1], ei[::-1], baseline=None, **kw)


def mine500(k):
    h = C[k]; return h / C[k + "_in"][1] / np.diff(mu_e)


def mine_i(k):
    h = C[k + "_i"]; return h / C[k + "_in"][1] / np.diff(i_e_mu)


def mean_curve(F2, k, a):            # mean of a published curve over its whole bins with mu >= cos(alpha)
    sel = mu_e[:-1] >= np.cos(np.radians(a)) - 1e-9
    return theirs500(F2, k)[sel].mean()


# ------------------------------------------------------------------ cone MC vs published
P("# 1. Repo opaque-cone MC (Lambertian) vs Ahlberg+ Fig. 2 (top row, Lambertian), their 500 mu-bins")
P("# mean over whole bins with mu >= cos(alpha); outside: median of the ratio over bins 0.05 < mu < cos(alpha) - 0.01")
cases = [(f"a:alpha={a}", a, 3.0) for a in (5, 10, 15, 20, 25)] + [(f"b:R=1e{l}", 25, float(l)) for l in (1, 2, 4, 5)]
P("# shift: their curve vs ours moved by k bins toward the axis (np.roll(ours, k)); rms of ln(ours/theirs), bins with > 50 photons")
for k, a, lR in cases:
    t = theirs500(L, k); m = mine500(key(a, lR)); h = C[key(a, lR)]
    rms = {}
    for sh in (-2, -1, 0, 1, 2):
        ok = (h > 50) & (np.roll(h, sh) > 50) & (t > 0); ok[:3] = ok[-3:] = False
        rms[sh] = np.sqrt(np.mean(np.log(np.roll(m, sh)[ok] / t[ok]) ** 2))
    sel = mu_e[:-1] >= np.cos(np.radians(a)) - 1e-9
    so = (muc < np.cos(np.radians(a)) - 0.01) & (muc > 0.05)
    m1 = np.roll(m, 1)
    P(f"alpha={a:2d} R=1e{lR:.0f}: best shift {min(rms, key=rms.get):+d} (rms " + " ".join(f"{s:+d}:{v:.3f}" for s, v in rms.items()) + ")")
    P(f"   inside (bins {sel.sum()}): theirs {t[sel].mean():6.2f}  cone MC {m[sel].mean():6.2f} (ratio {m[sel].mean() / t[sel].mean():.3f})"
      f"  shifted by 1: {m1[sel].mean():6.2f} (ratio {m1[sel].mean() / t[sel].mean():.3f});"
      f"  outside median ratio {np.median(m[so] / t[so]):.3f}")
P("# 2. Their own Lambertian / Chandrasekhar ratio of the mean boost at i <= alpha, Fig. 2a (R = 1e3)")
for a in (10, 15, 20, 25):
    P(f"alpha={a}: B_L/B_Ch = {mean_curve(L, f'a:alpha={a}', a) / mean_curve(Ch, f'a:alpha={a}', a):.3f}")
P("# 3. Cone MC (Lambertian) mean boost / Ahlberg+ Fig. 4a (Chandrasekhar); rows alpha, columns R")
JS = (0, 10, 21, 31, 39)
P("R: " + " ".join(f"{10 ** s[j]:.4g}" for j in JS))
ratio = {}
for a in (10, 15, 20, 25, 30, 35, 40, 45):
    m = int(np.argmin(abs(alg - a))); row = []
    for j in JS:
        n_in, n = C[key(a, float(s[j])) + "_in"]
        b = n_in / n * Bmax(a); row.append(b / GB[m, j]); ratio[(a, j)] = row[-1]
    P(f"alpha={a:2d}: " + " ".join(f"{r:.3f}" for r in row))

fig, axs = plt.subplots(1, 3, figsize=(16, 4.9))
vir = colormaps["viridis"]
for k, a in enumerate((5, 10, 15, 20, 25)):
    col = vir(k / 4.6)
    stairs_theirs(axs[0], L, f"a:alpha={a}", color=col, lw=1.2, label=f"Ahlberg+ Fig. 2a, α = {a}°")
    axs[0].semilogy(icen, mine_i(key(a, 3.0)), "o", ms=2.6, color=col, mec="none")
blues = ["#191970", "#0c0cb8", "#0000ff", "#0066e6", "#00cdcd"]
for k, l in enumerate((1, 2, 3, 4, 5)):
    stairs_theirs(axs[1], L, f"b:R=1e{l}", color=blues[k], lw=1.2, label=f"Ahlberg+ Fig. 2b, R = 10$^{l}$")
    axs[1].semilogy(icen, mine_i(key(25, float(l))), "o", ms=2.6, color=blues[k], mec="none")
for ax, t in zip(axs[:2], ("(a) R = 10$^3$, Lambertian walls", "(b) α = 25°, Lambertian walls")):
    ax.plot([], [], "o", ms=3, color="#555", label="cone MC of the code, 1° bins")
    ax.set_yscale("log"); ax.set(xlim=(0, 90), ylim=(0.01, 60), xlabel="i [deg]", title=t)
    ax.yaxis.set_major_formatter(fmt); ax.grid(alpha=0.25); ax.legend(fontsize=7, loc="lower left")
axs[0].set_ylabel("B$_{\\rm L}$(i)")
grays = ["#c8c8c8", "#9a9a9a", "#6e6e6e", "#404040", "#111111"]
for k, j in enumerate(JS):
    A = (10, 15, 20, 25, 30, 35, 40, 45)
    axs[2].plot(A, [ratio[(a, j)] for a in A], "o-", color=grays[k], ms=5, lw=1.2, label=f"R = {10 ** s[j]:.3g}")
lc = [mean_curve(L, f"a:alpha={a}", a) / mean_curve(Ch, f"a:alpha={a}", a) for a in (10, 15, 20, 25)]
axs[2].plot((10, 15, 20, 25), lc, "D--", color="#c0392b", ms=6, lw=1.2, label="their B̄$_{\\rm L}$/B̄$_{\\rm Ch}$, Fig. 2a, R = 10$^3$")
axs[2].axhline(1, color="#888", lw=0.8)
axs[2].set(xlim=(7, 47), ylim=(0.9, 1.06), xlabel="α [deg]", ylabel="ratio of the mean boost at i ≤ α",
           title="(c) cone MC (Lambertian) / Ahlberg+ Fig. 4a (Chandrasekhar)")
axs[2].grid(alpha=0.25); axs[2].legend(fontsize=7, loc="lower right", ncol=2)
fig.tight_layout(); fig.savefig(f"{F}/ahlberg_published_vs_cone_mc.png", dpi=190, bbox_inches="tight")

# ------------------------------------------------------------------ transfer correction vs published
P("# 4. Mean boost at i < theta_c: C model (mc_transfer = 1, 0) and MC through the wind")
labs = [str(x) for x in W["labels"]]
we = W["mu_edges"]; wc = np.degrees(np.arccos(0.5 * (we[1:] + we[:-1])))
for lab in labs:
    tc = float(W[f"{lab}:theta_c"]); ctc = np.cos(np.radians(tc)); mu = W[f"{lab}:mu"]; kk = mu >= ctc
    b1 = np.trapezoid(W[f"{lab}:B1"][kk], mu[kk]) / (1 - ctc); b0 = np.trapezoid(W[f"{lab}:B0"][kk], mu[kk]) / (1 - ctc)
    n_in, n = W[f"{lab}:mc_in"]; bm = n_in / n / (1 - ctc)
    P(f"{lab:18s} theta_c {tc:5.1f}: C1 {b1:.2f}  MC {bm:.2f}  C0 {b0:.2f}  B_max {Bmax(tc):.2f}  share MC {n_in / n:.3f}"
      f"  int B1 dmu {np.trapezoid(W[f'{lab}:B1'], mu):.3f}  int B0 dmu {np.trapezoid(W[f'{lab}:B0'], mu):.3f}")
P("# 5. Ahlberg+ Fig. 4a at alpha = 31.25, 32.5, 45 deg")
for a in (31.25, 32.5, 45.0):
    m = int(np.argmin(abs(alg - a)))
    P(f"alpha={alg[m]:.2f}: " + ", ".join(f"R={10 ** s[j]:.4g}: {GB[m, j]:.2f}" for j in JS))
P("# 6. Shape: B(alpha - 1 deg)/B(~0) and B(alpha + 10 deg)/B(~0)")
for a in (20, 25):
    i, B = Ch[f"a:alpha={a}"].T; b0 = np.interp(1, i, B)
    P(f"Ahlberg+ Fig. 2a Ch, alpha={a}, R=1e3: {np.interp(a - 1, i, B) / b0:.3f}  {np.interp(a + 10, i, B) / b0:.3f}")
for lab in labs[:2]:
    tc = float(W[f"{lab}:theta_c"]); ii = np.degrees(np.arccos(W[f"{lab}:mu"]))[::-1]; B = W[f"{lab}:B1"][::-1]
    b0 = np.interp(5, ii, B)
    P(f"C mc_transfer=1 {lab}, theta_c={tc:.1f}: {np.interp(tc - 1, ii, B) / b0:.3f}  {np.interp(tc + 10, ii, B) / b0:.3f}")

fig, (ax, bx) = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw=dict(width_ratios=[1.1, 1]))
for k, a in enumerate((5, 10, 15, 20, 25)):
    stairs_theirs(ax, Ch, f"a:alpha={a}", color=vir(k / 4.6), lw=1.0, label=f"Ahlberg+ Fig. 2a, α = {a}°, R = 10$^3$")
for lab, col in zip(labs[:2], ("#c0392b", "#2f6bd6")):
    tc = float(W[f"{lab}:theta_c"]); ii = np.degrees(np.arccos(W[f"{lab}:mu"]))
    ax.semilogy(ii, W[f"{lab}:B1"], color=col, lw=2.2, label=f"C, mc_transfer = 1, θ$_c$ = {tc:.1f}°")
    ax.semilogy(ii, W[f"{lab}:B0"], color=col, lw=1.1, ls="--", label=f"C, mc_transfer = 0, θ$_c$ = {tc:.1f}°")
    h = W[f"{lab}:mc_counts"]; n = W[f"{lab}:mc_in"][1]; ok = h > 0
    ax.errorbar(wc[ok], (h / n / np.diff(we))[ok], yerr=(np.sqrt(h) / n / np.diff(we))[ok], fmt="o", ms=4, color=col,
                mec="white", mew=0.7, elinewidth=0.8, label=f"MC through the wind, θ$_c$ = {tc:.1f}°")
ax.axhline(1, color="#8a8a8a", lw=0.6, ls=":"); ax.set_yscale("log")
ax.set(xlim=(0, 90), ylim=(0.01, 60), xlabel="inclination i [deg]", ylabel="B(i) = L$_{\\rm iso}$(i) / L$_{\\rm total}$",
       title="(a) B(i): Ahlberg+ (Chandrasekhar walls) and NGC7793 BH3a")
ax.yaxis.set_major_formatter(fmt); ax.grid(alpha=0.25)
ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False)
for k, j in enumerate(JS):
    o = np.argsort(alg)
    bx.plot(alg[o], GB[o, j], color=grays[k], lw=1.6, label=f"Ahlberg+ Fig. 4a, R = {10 ** s[j]:.3g}")
al = np.linspace(6, 88, 300)
bx.plot(al, Bmax(al), color="#8a8a8a", lw=0.9, ls="--", label="B$_{\\max}$ = 1/(1 − cos α), their Eq. 7")
bx.axvspan(45, 90, color="#f2f2f2", lw=0); bx.text(46, 30, "beyond their grid\n(α ≤ 45°)", fontsize=8, color="#666")
for k, lab in enumerate(labs):
    tc = float(W[f"{lab}:theta_c"]); ctc = np.cos(np.radians(tc)); mu = W[f"{lab}:mu"]; kk = mu >= ctc
    b1 = np.trapezoid(W[f"{lab}:B1"][kk], mu[kk]) / (1 - ctc); b0 = np.trapezoid(W[f"{lab}:B0"][kk], mu[kk]) / (1 - ctc)
    n_in, n = W[f"{lab}:mc_in"]; f0 = k == 0
    bx.plot(tc, b1, "o", ms=7, color="#2f6bd6", mec="white", mew=1, label="C, mc_transfer = 1" if f0 else None, zorder=5)
    bx.plot(tc, n_in / n / (1 - ctc), "x", ms=8, mew=2, color="#2a9d55", label="MC through the wind" if f0 else None, zorder=6)
    bx.plot(tc, b0, "v", ms=7, color="#e07b00", mec="white", mew=1, label="C, mc_transfer = 0" if f0 else None, zorder=5)
bx.set_yscale("log")
bx.set(xlim=(5, 90), ylim=(1, 60), xlabel="funnel half-opening α = θ$_c$ [deg]", ylabel="mean boost at i < α",
       title="(b) mean boost inside the funnel (NGC7793 fits, ω varied)")
bx.set_yticks([1, 2, 3, 5, 10, 20, 50]); bx.yaxis.set_major_formatter(fmt); bx.yaxis.set_minor_formatter(mt.NullFormatter())
bx.grid(alpha=0.25); bx.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False)
fig.tight_layout(); fig.savefig(f"{F}/ahlberg_published_vs_mc_transfer.png", dpi=190, bbox_inches="tight")

open(f"{D}/summary.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
