# -*- coding: utf-8 -*-

import json
from watson_developer_cloud import ConversationV1

# input in Python 2.7 evals(), so lets not use it.
try: input = raw_input
except NameError: pass

### Conversation variables ###
# ctx you copy and paste straight from the conversation service credentials (if using new layout)
ctx = {
  "url": "https://gateway.watsonplatform.net/conversation/api",
  "password": "......",
  "username": "......"
}

# workspace id can be gotten by "view details" in the drop down menu of the conversation tile.
workspaceId = '24541008-3420-4a39-ba7d-b2ebf4337e2b'
##############################

conv = ConversationV1(version='2016-09-20', username=ctx.get('username'),password=ctx.get('password'))

context = {} 
i = ''

while i != '...':
    i = input()
    message = { 'text': i }
    if i != '...': 
        response = conv.message(workspace_id = workspaceId, message_input = message, context = context)
        context = response['context']
        print(json.dumps(response))
        #print(json.dumps(response['output']['text']))

