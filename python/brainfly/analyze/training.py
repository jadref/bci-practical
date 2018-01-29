#!/usr/bin/env python3
# Set up imports and paths
import sys
import os
import numpy as np

sys.path.append('../signalProc/')

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


def subsample_frequencies(freqs, width=4):
    width = int(np.ceil(len(freqs) / width))
    weights = np.ones(width) / width
    result = np.array([np.convolve(freqs[:, i], weights, 'same')[::width] for i in range(freqs.shape[1])]).T
    return result


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

freqs = np.linspace(0, hdr.fSample/2, len(data[0]))
data = [d[(5 <= freqs) & (freqs <= 32)] for d in data]
data = [subsample_frequencies(d, 4) for d in data]

with open('processed_data.pkl', 'wb') as f:
    pickle.dump({'X': data, 'events': events, 'hdr': hdr}, f)
# 7: train classifier, default is a linear-least-squares-classifier
import linear
# mapping = {('stimulus.target', 0): 0, ('stimulus.target', 1): 1}
classifier = linear.fit(data, events)  # ,mapping
print(f'number of features: {classifier.coef_.shape}')

# save the trained classifer
print('Saving clsfr to : %s' % (cname + '.pk'))
pickle.dump({'classifier': classifier,
             'bad_channels': bad_channels}, open(cname + '.pk', 'wb'))
