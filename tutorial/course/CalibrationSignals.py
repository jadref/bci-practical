import sys
sys.path.append('../../python/signalProc')
import pickle

import bufhelp

_, hdr = bufhelp.connect()
data, events, _ = bufhelp.gatherdata('stimulus.type', 600, 'experiment.end', milliseconds=True)

pickle.dump({
    'data': data,
    'events': events,
    'hdr': hdr,
}, open('training_data.pkl', 'wb'))
