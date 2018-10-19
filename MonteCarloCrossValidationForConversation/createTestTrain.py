# -*- coding: utf-8 -*-
# Author: Simon O'Doherty
# Unsupported.

import json
from random import randint

# Settings: 
workingDirectory = './workarea/'
conversationFile = 'conversation.json'
testPercent = 10    # percentage size of test set.

########### 
questionCount = 0
intentCount = 0 
testSize = 0

testNode = { "output":{ "text":"Monte Carlo Test Node" },
      "conditions":"context.monteCarloTest == true",
      "dialog_node":"montecarlo",
      "previous_sibling":"node_start"
    }

with open(workingDirectory + conversationFile) as json_data:
    source = json.load(json_data)

intents = source['intents']
intentCount = len(intents)

# Determine size of my test set.
for intent in intents: 
    questionCount += len(intent['examples'])
    
testSize = (questionCount / 100) * testPercent

for ts in xrange(0,3):
    with open(workingDirectory + conversationFile) as json_data:
        trainSet = json.load(json_data)
     
    for x in range(0,len(trainSet['dialog_nodes'])):
        if trainSet['dialog_nodes'][x]['previous_sibling'] == 'node_start':
            trainSet['dialog_nodes'][x]['previous_sibling'] = 'montecarlo'
    
    trainSet['dialog_nodes'].append(testNode)
        
    testSet = []
    for x in xrange(1,testSize):
        randomIntent = randint(0,(intentCount - 1))
        ecount = len(trainSet['intents'][randomIntent]['examples'])
        if ecount == 0:
            continue
        elif ecount > 1: 
            randomQuestion = randint(0, (ecount - 1))
        else: 
            randomQuestion = 0
        
        qa = []
        
        q = trainSet['intents'][randomIntent]['examples'][randomQuestion]['text']
        a = trainSet['intents'][randomIntent]['intent']

        qa.append(q)
        qa.append(a)

        testSet.append(qa)
        trainSet['intents'][randomIntent]['examples'].pop(randomQuestion)
     
    trainSet['name'] = 'TRAIN ' + str(ts + 1) + ': ' + trainSet['name']
    open(workingDirectory + conversationFile.replace('.json', '_train' + str(ts + 1) + '.json'), "w").write(
        json.dumps(trainSet, sort_keys=True, indent=4, separators=(',', ': '))
        )
    open(workingDirectory + conversationFile.replace('.json', '_test' + str(ts + 1) + '.txt'), "w").write(
        json.dumps(testSet, sort_keys=True, indent=4, separators=(',', ': '))
        )
    
print('Created Test and Train sets')
