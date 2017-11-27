import math
import pickle
import sys
sys.path.append('../../python/signalProc')

import numpy as np

import bufhelp
from bufhelp import FieldTrip
import preproc

def send_event(event_type, event_value, sample=-1, offset=0):
    """Custom send event to allow to manually specify sample"""
    ftc = bufhelp.ftc
    e = FieldTrip.Event()
    e.type = event_type
    e.value = event_value
    if offset>0 : 
        sample, bla = ftc.poll()
        e.sample = sample + offset + 1
    elif sample >= 0:
        e.sample = sample
    ftc.putEvents(e)

if __name__ == '__main__':
    with open('classifier.pkl', 'rb') as f:
        clf = pickle.load(f)

    ftc, hdr = bufhelp.connect()
    trial_length_ms = 600
    trial_length_samples = math.ceil((trial_length_ms/1000.)*hdr.fSample)

    # gather stores events that haven't been long enough ago to collect data
    gather = []
    print('Waiting for events...')
    while True:
        events = bufhelp.buffer_newevents('stimulus.type', timeout_ms=1000)
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
                data = preproc.detrend([data])
                data = preproc.spectralfilter(data, (0, 1, 14, 15), hdr.fSample)
                gather.remove(point)
                # Classify
                pred = clf.predict(np.array(data).reshape(1, -1))[0]
                send_event('classifier.prediction', pred, evt.sample)
