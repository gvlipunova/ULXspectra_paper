# Generates the rows of tab:bestfit_params (sections/10_results.tex) from ULXspectra-mc b551655 summaries.
# Run: python3 figures/make_bestfit_params_table.py
import math, csv
B='/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra-mc/'
fits=[l.split()[0] for l in open(B+'docs/scripts/mc_table/best_refits.txt') if l.strip() and l[0]!='#'][:14]+['NGC247S.BH3a']
chi={}
for r in csv.DictReader(open(B+'summaries/best_refit_per_source.tsv'),delimiter='\t'):
    chi[r['source']+'.'+r['preset']]=(float(r['chi2']),int(r['n_points']))
chi['NGC247S.BH3a']=(0.133,27)
# summaries/mc_vs_nomc_BH3a_BH4a.tsv / check tsv
def post(f):
    d=B+'summaries/best_refit_spectra/'+f if f!='NGC247S.BH3a' else '/aux/muses01b/glipunova/rabota/ULX_spectra/mcmcfit/ULXspectra-refit/results/mcmc_NGC247S.BH3a.mc_0p3-10keV'
    P={};on=False
    for l in open(d+'/posterior_summary.txt'):
        if 'physical parameters' in l: on=True; continue
        if on and l.strip() and l[0]!='#':
            s=l.split(); P[s[0]]=tuple(map(float,s[1:4]))
    return P
def fl(m,lo,hi):  # log10 with errors
    return f"${math.log10(m):.2f}^{{+{math.log10((m+hi)/m):.2f}}}_{{-{math.log10(m/(m-lo)) if m-lo>0 else 9:.2f}}}$"
def fv(m,lo,hi,nd=2):
    return f"${m:.{nd}f}^{{+{hi:.{nd}f}}}_{{-{lo:.{nd}f}}}$"
for f in fits:
    s,p=f.split('.');P=post(f);c,n=chi[f]
    ns=p.startswith('NS')
    m='$1.4$' if ns else fl(*P['log_m_bh'])
    md=fl(*P['log_mdot0'])
    ii=P['incl_deg']; i=fv(*ii,nd=1 if max(ii[1],ii[2])<1 else 0)
    ew=fv(*P['eps_w']) if 'eps_w' in P else ('$0.5$' if ns else '--')
    if ns:
        x=P['log_wind_inner_launch_x']; rin=fl(4.5*x[0],4.5*x[1],4.5*x[2])[:-1]+'{}^\\dagger$'
    else:
        r=P['r_in_factor']; rin=fv(*r,nd=1 if r[2]>0.05 else 2)
    rout=fl(*P['log_r_out_factor'])
    fin=fv(*P['user_mdot_in_fraction']) if 'user_mdot_in_fraction' in P else '--'
    ex=[]
    if 'beta_w' in P: ex.append(r'$\beta_{\rm w}$ '+fv(*P['beta_w'],nd=1))
    if 'omega_frac' in P: ex.append(r'$\Omega_{\rm w}/4\pi$ '+fv(*P['omega_frac'],nd=3))
    if 'log_magn_eta' in P: ex.append(r'$\log\eta_{\rm magn}$ '+fl(*P['log_magn_eta']))
    print(f"{s} & {p} & {c:.3g}/{n} & {m} & {md} & {i} & {ew} & {rin} & {rout} & {fin} & {'; '.join(ex) or '--'} \\\\")
