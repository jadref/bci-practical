# Imports
import sys
import os
import pickle

try:
    pydir = os.path.dirname(__file__)
except ImportError:
    pydir = os.getcwd()

sys.path.append(os.path.join(os.path.abspath(pydir), '../../signalProc'))
import bufhelp
import h5py

# connect to buffer
ftc, hdr = bufhelp.connect()

# Constants
trlen_ms = 3000
dname = 'training_data'
cname = 'clsfr'

data, events, stopevents = bufhelp.gatherdata("stimulus.target",
                                              trlen_ms,
                                              ("stimulus.training", "end"),
                                              milliseconds=True)
pickle.dump({"events": events,
             "data": data,
             'hdr': hdr
             }, open(dname+'.pk', 'wb')
            )
