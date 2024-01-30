import json
# import os
from google.cloud import pubsub_v1

# this os.getenv shoud work in python 3.7
# project_id = os.getenv('GCP_PROJECT')
# changed python to 3.11
project_id = 'smartsheet-api-functions'
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
        sheetid = request_json["scopeObjectId"]
        print("sheetid : ", sheetid)
        events = request_json["events"]
        for event in events:
            print('------ event ------')
            print(event)
            objectType = event['objectType']
            print("objectType : ", objectType)
            eventType = event['eventType']
            print("eventType : ", eventType)
        short_request_json = request_json
        short_request_json.pop("nonce",None)
        short_request_json.pop("scope",None)
        for event in short_request_json["events"]:
            event.pop("timestamp",None)
            event.pop("userId",None)
        publish_request_json(short_request_json)
        # print("call back publlish result ", publish_result)
        return json.dumps({
             "callback from smartsheet sheet id ": sheetid
        })
    else:
      	return 'neither smartsheet challenge nor callback'

def publish_request_json(short_request_json):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    data = str(short_request_json)
    data = data.encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    print(future.result())
    print("Published messages.")
    # retrun future.result()
