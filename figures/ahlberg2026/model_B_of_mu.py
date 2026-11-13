"""C model L_iso(mu) with mc_transfer = 1 and 0 on a fine mu grid, for one run (+ name=value sets).
Usage (from the ULXspectra repo): python3 compute_C.py RUNDIR OUTNPZ [name=value ...]"""
import os, sys, io, contextlib, numpy as np
RUNDIR, OUT = sys.argv[1].rstrip("/"), sys.argv[2]
SETS = [a.split("=", 1) for a in sys.argv[3:]]
name = os.path.basename(RUNDIR)[5:]
os.environ["MODEL_PRESET"] = name.split(".")[1]
sys.path.insert(0, os.getcwd())
from psrcs.run_overrides import from_run_dir
from_run_dir(RUNDIR)
with contextlib.redirect_stdout(io.StringIO()):
    from psrcs.params_mcmc import theta_to_params
    from psrcs.model_mcmc import model_components_from_pars
    from psrcs.diagnostics import make_py_params_from_dict
    best = np.atleast_1d(np.loadtxt(os.path.join(RUNDIR, "best_params.txt")))
    pars = theta_to_params(best)
    for k, v in SETS:
        pars[k] = type(pars[k])(float(v))
    p = make_py_params_from_dict(pars)
SIGMA = 5.670374e-5
E = np.logspace(-2.5, 1.5, 9)
mu = np.linspace(0.0025, 0.9975, 200)
res = {}
for mct in (1, 0):
    L = []
    for m in mu:
        q = dict(pars, incl_deg=float(np.degrees(np.arccos(m))), mc_transfer=mct)
        with contextlib.redirect_stdout(io.StringIO()):
            _, _, _, dg = model_components_from_pars(E, q)
        L.append(dg["Lbol_total"] / (SIGMA * p.r_in ** 2))
    res[f"L{mct}"] = np.array(L)
    res[f"Lemit{mct}"] = (dg["L_disc_direct"] + dg["L_wind_bol_cal_corr"]) / (SIGMA * p.r_in ** 2)
np.savez(OUT, mu=mu, omega=pars["omega_frac"], **res)
print(OUT, "omega", pars["omega_frac"], "int L1 dmu / Lemit", np.trapezoid(res["L1"], mu) / res["Lemit1"], "mct0:", np.trapezoid(res["L0"], mu) / res["Lemit0"])
