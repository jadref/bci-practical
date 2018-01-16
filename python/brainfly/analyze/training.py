#!/usr/bin/env python3
# Set up imports and paths
import sys
import os
import numpy as np

sys.path.append('../../signalProc/')

import bufhelp
import preproc
import pickle

dname = 'training_data'
cname = 'clsfr'

print("Training classifier")
f = pickle.load(open(dname + '.pk', 'rb'))
data = f['data']
events = f['events']
hdr = f['hdr']

# -------------------------------------------------------------------
#  Run the standard pre-processing and analysis pipeline
# 1: detrend
data = [d[:, :10] for d in data]
data = preproc.detrend(data)
# 2: bad-channel removal
data, bad_channels = preproc.badchannelremoval(data)
print(f'Removed channels: {bad_channels}')
# 3: apply spatial filter
data = preproc.spatialfilter(data, type='car')
# 4 & 5: map to frequencies and select frequencies of interest
data = preproc.spectralfilter(data, (5, 6, 31, 32), hdr.fSample)
# 6 : bad-trial removal
data, events, bad_trials = preproc.badtrialremoval(data, events)
print(f'Removed trials: {bad_trials}')
# 7: train classifier, default is a linear-least-squares-classifier
import linear
# mapping = {('stimulus.target', 0): 0, ('stimulus.target', 1): 1}
classifier = linear.fit(data, events)  # ,mapping)

# save the trained classifer
print('Saving clsfr to : %s' % (cname + '.pk'))
pickle.dump({'classifier': classifier}, open(cname + '.pk', 'wb'))
