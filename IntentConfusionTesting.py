# Note: The code below is a sample provided to illustrate one way 
# to approach this issue and is used as is and at your own risk. In order 
# for this example to perform as intended, the script must be laid out exactly 
# as indicated below. This script will not be customized for specific 
# environments or applications.
#
# @author: Simon O'Doherty


from watson_developer_cloud import ConversationV1
import pandas as pd
from scipy.cluster.vq import kmeans, vq
import numpy as np

# Get these details from your service credentials. 
ctx = {
  "url": "https://gateway.watsonplatform.net/assistant/api",
  "password": "...",
  "username": "..."
}
workspace_id = '6f34419b-6a9f-4817-b5b5-4650682443f5';

# This is used to append to a question, to prevent 100% match.
safeword = 'SIO'

wa = ConversationV1(
    username=ctx.get('username'), 
    password=ctx.get('password'), 
    version='2018-09-20', 
    url=ctx.get('url')
)

# Send message to WA, and return output, intents and context.
def message(text='',context=None):
    msg = {'text': text}
    response = wa.message(workspace_id=workspace_id, input=msg, context=context, alternate_intents=True)
    
    result = response.result
    output = result['output']['text']
    context = result['context']
    intents = result['intents']
    
    return (output, intents, context)


# Get the list of intents and their example questions.
def getIntents():
    response = wa.get_workspace(workspace_id=workspace_id, export=True)
    return response.result['intents']


# Uses K-Means to deteremine if the question was confused with another intent. 
def confusedQuestion(intents, question):
    
    ic = []
    for i in intents:
        ic.append(i['confidence'])
    
    v = np.array(ic)
    codebook, _ = kmeans(v,2)
    ci, _ = vq(v,codebook)
    
    # We want to make everything in the top bucket to have a value of 1.
    if ci[0] == 0: ci = 1-ci
    
    
    if sum(ci) > 1:
        r = {
            'question': question,
            'intent': intents[0]['intent'],
            'confused_with': intents[1]['intent']
            }
         
        return True, r
    
    
    return False, ''

## --- 

intents = getIntents()

print('Intent total: {}'.format(len(intents)))

recs = []
for intent in intents:
    print('{}'.format(intent['intent']))
    for example in intent['examples']:
        o,i,c = message(text='{} {}'.format(safeword,example['text']),context={})
        
        confused, response = confusedQuestion(i,example['text'])
        
        if confused:
            recs.append(response)
            print('    {} = {} . Confused with: {}'.format(
                response['question'], response['intent'], response['confused_with'])
            )
 
df = pd.DataFrame(recs, columns=['question','intent','confused_with'])
df.to_csv('confusion_report.csv')

print('\nDone.')