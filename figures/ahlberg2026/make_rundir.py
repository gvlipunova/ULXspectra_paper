# Make a RUNDIR (best_params.txt, run_settings.json) from a tests/reference npz, and check the round trip
import sys, os, json, subprocess, numpy as np
ref, outroot = sys.argv[1], sys.argv[2]
d = np.load(ref, allow_pickle=True); P = json.loads(str(d['pars_json']))
run = os.path.basename(ref)[:-4]                      # mcmc_SRC.PRESET.TAG
preset = run.split('.')[1]
code = f"""
import os, sys, json, numpy as np
os.environ['MODEL_PRESET']={preset!r}
sys.path.insert(0, os.getcwd())
from psrcs.config_mcmc import FREE_PARAMS
from psrcs.params_mcmc import theta_to_params
P=json.loads({json.dumps(json.dumps(P))})
theta=np.array([P[k] for k in FREE_PARAMS]); q=theta_to_params(theta)
diff={{k:(q.get(k),v) for k,v in P.items() if (q.get(k)!=v and not (isinstance(v,float) and isinstance(q.get(k),(int,float)) and abs(q.get(k)-v)<=1e-12*max(1,abs(v))))}}
print(json.dumps({{'free':list(FREE_PARAMS),'theta':theta.tolist(),'diff':{{k:[str(a),str(b)] for k,(a,b) in diff.items()}}}}))
"""
r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True)
out = json.loads(r.stdout.strip().splitlines()[-1])
rd = os.path.join(outroot, run); os.makedirs(rd, exist_ok=True)
np.savetxt(os.path.join(rd, 'best_params.txt'), out['theta'])
sets = {k: b for k, (a, b) in out['diff'].items()}
json.dump({'set': sets}, open(os.path.join(rd, 'run_settings.json'), 'w'))
print(run, 'free', out['free'], '\n differing from preset ->set:', out['diff'])
