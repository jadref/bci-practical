import math
import pickle
import sys

import numpy as np

sys.path.append('../signalProc')
import bufhelp
import preproc


def subsample_frequencies(freqs, width=4):
    width = int(np.ceil(len(freqs) / width))
    weights = np.ones(width) / width
    result = np.array([np.convolve(freqs[:, i], weights, 'same')[::width] for i in range(freqs.shape[1])]).T
    return result


if __name__ == '__main__':
    with open('clsfr.pk', 'rb') as f:
        classifier = pickle.load(f)
        clf = classifier['classifier']
        bad_channels = classifier['bad_channels']
        good_channels = np.ones(10, dtype=np.bool)
        good_channels[bad_channels] = False

    ftc, hdr = bufhelp.connect()
    trlen_ms = 3000
    trial_length_samples = math.ceil((trlen_ms / 1000) * hdr.fSample)

    # gather stores events that haven't been long enough ago to collect data
    gather = []
    print('Waiting for events...')
    while True:
        events = bufhelp.buffer_newevents('experiment.predict', timeout_ms=1000)
        for evt in events:
            end_sample = evt.sample + trial_length_samples - 1
            gather.append((evt, end_sample))

        # Current sample count
        nSamples = bufhelp.globalstate[0]
        for point in gather:
            evt, end_sample = point
            if end_sample < nSamples:
                # Enough time has passed to collect the data
                data = ftc.getData((evt.sample, end_sample))
                # Preprocess
                data = data[:, :10]
                data = preproc.detrend([data])
                data[0] = data[0][:, good_channels]
                data = preproc.spatialfilter(data, type='car')
                data = preproc.spectralfilter(data, (5, 6, 31, 32), hdr.fSample)
                freqs = np.linspace(0, hdr.fSample/2, len(data[0]))
                data = [d[(5 <= freqs) & (freqs <= 32)] for d in data]
                data[0] = subsample_frequencies(data[0]).reshape(-1)
                gather.remove(point)
                # Classify
                data[0] = data[0]
                pred = clf.predict_proba(data)[0][1]
                print(pred)
                bufhelp.sendEvent('classifier.prediction', pred)
