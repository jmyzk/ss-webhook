# ss-webhook

This ww-webhook is a code of family of codes that handle smartsheet webhook.
The family of codes are:

ss-create-webhook: create webhook
ss-webhook: respond to webhook
ss-update: update sheet with mysql, one of a possible respose to a callback 
ss-delete-webhook: delete webhook

More information is available in each reqpository's readme.md.

What ss-webhook does:

1 listen to the callback url created by google cloud functions
2 if it get request
  and if it is challenge 
    it will respond to enable the webhook
3 if it is not a challenge = callback
    it will publish the sheet id to pubsub topic ss-webhook
    
