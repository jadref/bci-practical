import sys
sys.path.append('../../python/signalProc')
import pickle
import numpy as np

import bufhelp

ftc, hdr = bufhelp.connect()

data, events, _ = bufhelp.gatherdata('stimulus', 600, 'experiment.end', milliseconds=True)

with open('training_data.pk', 'wb') as f:
    pickle.dump({
        'data': data,
        'events': events,
        'hdr': hdr
    }, f)
