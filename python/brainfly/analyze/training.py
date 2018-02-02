"""
Load data collected during the training phase, preprocess it and train
a Logistic Regression classifier. The classifier is saved
to a pickle file.
"""
# Set up imports and paths
import sys
import os
import numpy as np

sys.path.append('../signalProc/')

import bufhelp
import util
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

with open('processed_data.pkl', 'wb') as f:
    pickle.dump({'X': data, 'events': events, 'hdr': hdr}, f)

# Reduce the number of features per channel
freqs = np.linspace(0, hdr.fSample/2, len(data[0]))
data = [d[(5 <= freqs) & (freqs <= 32)] for d in data]
data = [util.subsample_frequencies(d, 4) for d in data]

# 7: train classifier
import linear
# mapping = {('stimulus.target', 0): 0, ('stimulus.target', 1): 1}
classifier = linear.fit(data, events)  # ,mapping
print(f'number of features: {classifier.coef_.shape}')

# save the trained classifer
print('Saving clsfr to : %s' % (cname + '.pk'))
pickle.dump({'classifier': classifier,
             'bad_channels': bad_channels}, open(cname + '.pk', 'wb'))
