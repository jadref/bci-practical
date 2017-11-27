# Imports
from .algorithms_brainfly import algorithms_brainfly

# Paths
dataRootdir = '~/data/bci'
bufferpath = "../../dataAcq/buffer/python"
sigProcPath = "../signalProc"

# Constants
trlen_ms = 750 # trial length in 750 ms
label = 'movement'
make_plots = False
analysisType = 'ERSP'

algorithms_to_run = algorithms_brainfly()