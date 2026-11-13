# numpy>=2 shim (np.trapz removed), then run the repository's MC script unchanged
import sys, runpy, numpy
if not hasattr(numpy, "trapz"):
    numpy.trapz = numpy.trapezoid
script = sys.argv[1]; sys.argv = sys.argv[1:]
runpy.run_path(script, run_name="__main__")
