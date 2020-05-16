
# [START gae_python37_app]
from flask import Flask
from flask import request
from google.cloud import firestore
from datetime import datetime
import logging

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/',methods = ['GET', 'POST'])
def process():
    """Return a friendly HTTP greeting."""
    db = firestore.Client() #create db client

    if (request.method == 'GET'):
        #get from firestore with sql query
        data = request.args
        size = data["size"]
        date = data["date"]

        long = data["longitude"]
        lat = data["latitude"]

        query = db.collection(u'avalanches')\
            .where(u'size', u'>=', sizeParse(size))\
            .where(u'dateTime',u'>=',timeParse(date))

        results = []
        for item in query.stream():
            results.append(item.to_dict())

        results = distFilter(results)

        return results

    elif (request.method == 'POST'):
        #store data in firestore
        data = request.get_json()
        id = data["time"]
        data["dateTime"] = strToTime(data["time"])
        db.collection(u'avalanches').document(id).set(data)
        return str(data)

def strToTime(x):
    return datetime.strptime(x,"%Y%m%d_%H%M%S")

def sizeParse(rawSz):
    #returns size from spinner strings
    if rawSz == "Any":
        return 1
    else:
        return int(rawSz[0]) #first character

def timeParse(rawTime):
    #returns time limit from spinner value
    today = datetime.datetime.now()
    if rawTime == "Last Year":
        return today - datetime.timedelta(days=365)
    elif rawTime == "Last Month":
        return today - datetime.timedelta(days=31)
    elif rawTime == "Last Week":
        return today - datetime.timedelta(days=7)
    elif rawTime == "Last 3 Days":
        return today - datetime.timedelta(days=3)
    elif rawTime == "Last 24 Hours":
        return today - datetime.timedelta(days=1)
    #fallback
    return today - datetime.timedelta(days=365)


def distFilter(query,distance):
    #filters entries for those within a distance
    return 0

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]