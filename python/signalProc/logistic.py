import sklearn.linear_model
import skwrap

def fit(data, events, mapping=None):
    classifier = sklearn.linear_model.LogisticRegression()
    params = {"fit_intercept": [True]}
    skwrap.fit(data, events, classifier, mapping, params, reducer="mean")
    return classifier
    
def predict(data):
    global classifier    
    return skwrap.predict(data, classifier, reducerdata="mean")
