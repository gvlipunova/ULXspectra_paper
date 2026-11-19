# Rows of tab:mc_bestfits (sections/A3_monte_carlo.tex) from ULXspectra-mc summaries/mc_check_best_refits.tsv.
# Run: python3 figures/make_mc_bestfits_table.py [path to ULXspectra-mc]
import csv, sys
B = sys.argv[1] if len(sys.argv) > 1 else '/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra-mc'
R = {r['name']: r for r in csv.DictReader(open(B + '/summaries/mc_check_best_refits.tsv'), delimiter='\t')}
best = [l.split()[0] for l in open(B + '/docs/scripts/mc_table/best_refits.txt') if l.strip() and l[0] != '#'][:14]
best.sort(key=lambda n: (float(R[n]['incl']) >= float(R[n]['theta_c']), float(R[n]['incl'])))
def g(x):
    x = float(x); return f"{x:.3g}" if x < 100 else f"{x:.0f}"
for n in best + ['NGC247S.BH3a']:
    r = R[n]; s, p = n.split('.')
    lab = f"{s} {p}" + (" (2nd best)" if n == 'NGC247S.BH3a' else "")
    noise = float(r['chi2_noise'])
    print(f"{lab} & ${float(r['incl']):.1f}^\\circ$ (${float(r['theta_c']):.1f}^\\circ$) & "
          f"{float(r['Liso_off']):.2f} $\\to$ {float(r['Liso_on']):.2f} & {float(r['ratio_min']):.2f}--{float(r['ratio_max']):.2f} & "
          f"{g(r['chi2_fit'])} $\\to$ {g(r['chi2_mc'])}" + (f" ({noise:.1f})" if noise > 1 else "") + " \\\\")
