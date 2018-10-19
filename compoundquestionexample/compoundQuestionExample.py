# -*- coding: utf-8 -*-
# @author: sodoherty

from watson_developer_cloud import ConversationV1
from scipy.cluster.vq import kmeans, vq
import numpy as np

# By reading the confidences, it tries to guess if the user asked two questions.
def compoundQuestion(intents):
    v = np.array(intents)
    codebook, _ = kmeans(v,2)
    ci, _ = vq(v,codebook)
    
    # We want to make everything in the top bucket to have a value of 1.
    if ci[0] == 0: ci = 1-ci
    if sum(ci) == 2: return True
    return False

#########################  Conversation code.

# Bluemix Service credentials. 
ctx = {
  "url": "https://gateway.watsonplatform.net/conversation/api",
  "password": "...",
  "username": "..."
}
workspace_id = '...';

# Version number enables absolute confidences. 
conv = ConversationV1(version='2017-02-03', username=ctx.get('username'),password=ctx.get('password'))

context = {}
i = ''

# Initial response is conversation_start
response = conv.message(workspace_id = workspace_id, message_input = { 'text': '' }, context = context)
context = response['context']
print(response['output']['text'][0])
 
# Keep running until user types ...
while i != '...':
    i = input()
    message = { 'text': i }
    if i != '...': 
        response = conv.message(workspace_id = workspace_id, message_input = message, context = context, alternate_intents = True)
        context = response['context']

        # Here we try to determine if it is a compound question, and send values if it is.
        intent_confidences = list(o['confidence'] for o in response['intents'])
        if (compoundQuestion(intent_confidences)):
            context['primaryIntent'] = response['intents'][0]['intent']
            context['secondaryIntent'] = response['intents'][1]['intent']
            context['primaryConfidence'] = response['intents'][0]['confidence']
            context['secondaryConfidence'] = response['intents'][1]['confidence']
            message = {'text': 'compoundquestion'}
            response = conv.message(workspace_id = workspace_id, message_input = message, context = context, alternate_intents = True)
            context = response['context']
        
        # return Watsons response.
        print('> ' + response['output']['text'][0])
