#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("queryResult").get("action") != "Covid19CasesAction":
        return {}
    result = req.get("queryResult")
    parameters = result.get("parameters")
    zone = parameters.get("Covid19Country")

    cost = {'USA':'Total-5,87,173 Active-5,26,581', 'India':'Total-10,541 Active-8,978', 'Germany':'Total-1,30,072 Active-58,678', 'Italy':'Total-1,59,516 Active-1,03,616', 'France':'Total-1,36,779 Active-94,094'}

    speech = "Covid19 cases in " + zone + " is " + str(cost[zone])

    return {
            "fulfillmentText": speech,

    }




        #"speech": speech,
        #"displayText": speech,
        #"data": {},
        #"contextOut": [],
        #"source": "Covid19CasesIntent"


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
