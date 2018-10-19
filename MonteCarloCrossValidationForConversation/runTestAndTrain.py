# -*- coding: utf-8 -*-
# Author: Simon O'Doherty
# Unsupported

import json
from watson_developer_cloud import ConversationV1

###########################
workingDirectory = './workarea/'
filePrefix = 'conversation'

# Service credentials. Make sure all test workspaces are in the same service.
ctx = {}

workspace_ids = [
    '',
    '',
    ''
    ] 
###########################

version = '2016-09-20'
context = { 'monteCarloTest': True, 'expected_intent': 'none' }
message = { 'text': 'Hi'}
alternate_intents = True

for ts in xrange(0,3):
    print ('Running Test Set ' + str(ts + 1))

    conv = ConversationV1(version=version, username=ctx.get('username'),password=ctx.get('password'))
    response = conv.message(workspace_id = workspace_ids[ts], message_input = message, context = context)
    context = response['context']

    logs = 'Question\tExpected\tRecall@\tIntent\tConfidence\tMatched\n'

    with open(workingDirectory + filePrefix + '_test' + str(ts + 1) + '.txt') as json_data:
        source = json.load(json_data)
        
    for row in source: 
        message['text'] = row[0]
        context['expected_intent'] = row[1]
        response = conv.message(workspace_id = workspace_ids[ts], message_input = message, context = context, alternate_intents = alternate_intents)
        
        print('  ' + row[0])
        
        for i in xrange(0,len(response['intents'])):
            intent = response['intents'][i]['intent']

            logs += row[0] + '\t'
            logs += row[1] + '\t'
            logs += str(i + 1) + '\t'
            logs += intent + '\t'
            logs += str(response['intents'][i]['confidence']) + '\t'
            if row[1] == intent: 
                logs += 'Yes'
            else:
                logs += 'No'
            logs += '\n'
    
    # Writing it out as UTF-16 with BOM so that it will render content correctly in excel.
    open(workingDirectory + filePrefix + '_report' + str(ts + 1) + '.tsv', 'w').write('\ufeff' + logs.encode('UTF-16'))
