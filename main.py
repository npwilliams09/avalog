
# [START gae_python37_app]
from flask import Flask
from flask import request
from google.cloud import firestore

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/',methods = ['GET', 'POST'])
def process():
    """Return a friendly HTTP greeting."""
    db = firestore.Client() #create db client

    if (request.method == 'GET'):
        #get from firestore with sql query
        return str(db.collection(u'avalanches').where(u'size', u'==', u'1'))

    if (request.method == 'POST'):
        #store data in firestore
        data = request.form
        db.collection(u'avalanches').document(u'dummy').set(data)
        return 'data posted'




if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]