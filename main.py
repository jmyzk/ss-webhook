import json
import os
from google.cloud import pubsub_v1

# this os.getenv shoud work in python 3.7
project_id = os.getenv('GCP_PROJECT')
topic_name = 'ss-webhook'

def ss_webhook_responder(request):
    request_json = request.get_json()

    # for a webhook challenge, return verification
    if request.args and "challenge" in request.args:
        return 'not smartsheet challenge'
    elif request_json and "challenge" in request_json:
        return json.dumps({
            "smartsheetHookResponse": request_json['challenge']
        })

    # if this is a callback
    elif request_json and "scopeObjectId" in request_json:
        print(type(request_json))
        sheetid = request_json["scopeObjectId"]
        print("sheetid : ", sheetid)
        events = request_json["events"]
        for event in events:
            objectType = event['objectType']
            print("objectType : ", objectType)
            eventType = event['eventType']
            print("eventType : ", eventType)
        publish_result = publish_request_json(request_json)
        print("call back publlish result ", publish_result)
        return json.dumps({
             "callback from smartsheet sheet id ": sheetid
        })
    else:
      	return 'neither smartsheet challenge nor callback'

def publish_request_json(request_json):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    data = str(request_json)
    data = data.encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    print(future.result())
    print("Published messages.")
    retrun future.result()
