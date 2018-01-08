#!/usr/bin/env python3
# Set up imports and paths
import sys, os
import numpy as np

# Get the helper functions for connecting to the buffer
try:
    pydir = os.path.dirname(__file__)
except:
    pydir = os.getcwd()
sigProcPath = os.path.join(os.path.abspath(pydir), '../../python/signalProc')
sys.path.append(sigProcPath)
import bufhelp
import preproc
import pickle

dname = 'training_data'
cname = 'clsfr'

print("Training classifier")
if os.path.exists(dname + '.pk'):
    f = pickle.load(open(dname + '.pk', 'rb'))
    data = f['data']
    events = f['events']
    hdr = f['hdr']

# -------------------------------------------------------------------
#  Run the standard pre-processing and analysis pipeline
# 1: detrend
data = preproc.detrend(data)
# 2: bad-channel removal
data, badch = preproc.badchannelremoval(data)
# 3: apply spatial filter
data = preproc.spatialfilter(data, type='car')
# 4 & 5: map to frequencies and select frequencies of interest
data = preproc.spectralfilter(data, (0, 1, 14, 15), hdr.fSample)
# 6 : bad-trial removal
data, events, badtrials = preproc.badtrailremoval(data, events)
# 7: train classifier, default is a linear-least-squares-classifier
import linear

# mapping = {('stimulus.target', 0): 0, ('stimulus.target', 1): 1}
classifier = linear.fit(data, events)  # ,mapping)

# save the trained classifer
print('Saving clsfr to : %s' % (cname + '.pk'))
pickle.dump({'classifier': classifier}, open(cname + '.pk', 'wb'))
