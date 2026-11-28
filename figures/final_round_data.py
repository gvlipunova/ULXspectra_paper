"""Fits of the final round (second version of the paper) for the paper's own figure scripts.

Data: ULXspectra-mc summaries/final_round_all_fits.tsv and final_round_best_per_source.tsv
(docs/scripts/final_round_summary.py, commit 9fc8e3c; for_paper_session Note 18, item 7), and the run
directories they name (results/ of the ULXspectra working copy, which all worktrees share).
Run tags mc28/mc28b/mc28c/mc30/mc32 (code commits afaa8b3/b08b4df/54a9e72/70a23eb/a650c54).

Rows of the figures: the sources of tab:sources in its order, NGC247SS twice (0.3-10 keV and 0.3-1.7 keV,
Notes 15-16; the author chose both bands, 2026-11-28).
"""
import csv

B_DEFAULT = "/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra-mc"
RES = "/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra"   # run_dir is relative to this

FULL, SOFT = "0.3-10 keV", "0.3-1.7 keV"
# (row label, source, band, type in tab:sources: "BH" BH candidate, "NS" PULX or NS candidate, None unknown)
ROWS = [("HolmII", "HolmII", FULL, "BH"), ("HolmIX", "HolmIX", FULL, "BH"), ("M101ULS", "M101ULS", FULL, "BH"),
        ("M51ULS", "M51ULS", FULL, "NS"), ("M81ULS", "M81ULS", FULL, "NS"), ("NGC1313B", "NGC1313B", FULL, "BH"),
        ("NGC1313H", "NGC1313H", FULL, "NS"), ("NGC247S", "NGC247S", FULL, None),
        ("NGC247SS", "NGC247SS", FULL, None), ("NGC247SS, <1.7 keV", "NGC247SS", SOFT, None),
        ("NGC300", "NGC300", FULL, "NS"), ("NGC5408", "NGC5408", FULL, "BH"), ("NGC55", "NGC55", FULL, "BH"),
        ("NGC6946", "NGC6946", FULL, "BH"), ("NGC7793", "NGC7793", FULL, "NS")]
# Fits that fail the Monte Carlo check (Note 15/16: NGC247SS NS5ar over 0.3-10 keV). NGC247S BH4a passes in
# the final round (Note 18, item 7).
FAILS_MC = {("NGC247SS", FULL, "NS5ar")}
# Best fit of the source in tab:bestfit_params where it differs from the lowest chi2 (Note 16: NGC247SS 0.3-10 keV
# is BH4a, because NS5ar fails the MC check).
TABLE6_OVERRIDE = {("NGC247SS", FULL): "BH4a"}


def load(b=B_DEFAULT):
    """Selected fit per (source, band, preset), and the best-per-source rows keyed by (source, band)."""
    fits = {}
    for r in csv.DictReader(open(b + "/summaries/final_round_all_fits.tsv"), delimiter="\t"):
        if r["selected"] == "yes":
            fits[(r["source"], r["band"], r["preset"])] = r
    best = {(r["source"], r["band"]): r
            for r in csv.DictReader(open(b + "/summaries/final_round_best_per_source.tsv"), delimiter="\t")}
    return fits, best


def table6_preset(best, src, band):
    return TABLE6_OVERRIDE.get((src, band), best[(src, band)]["best"])


def best_params(fit):
    """Best-fit point of a run: {parameter: value} from best_params.txt."""
    lines = open(f"{RES}/{fit['run_dir']}/best_params.txt").read().splitlines()
    names = [w for w in lines[0].lstrip("#").split() if "=" not in w]
    return dict(zip(names, map(float, lines[1].split())))


def posterior(fit, name):
    """(median, minus, plus) of a physical parameter from posterior_summary.txt (linear M for log_m_bh)."""
    on = False
    for l in open(f"{RES}/{fit['run_dir']}/posterior_summary.txt"):
        if "physical parameters" in l:
            on = True
        elif on and l.split() and l.split()[0] == name:
            return tuple(map(float, l.split()[1:4]))
    raise KeyError((fit["run_dir"], name))
