import time

from googleapiclient import discovery
import os

from googleapiclient.errors import HttpError

os.environ['http_proxy'] = 'http://localhost:7890'
os.environ['https_proxy'] = 'http://localhost:7890'

API_KEY = 'XXXXX'

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

# analyze_request = {
#   'comment': { 'text': 'friendly greetings from python' },
#   'requestedAttributes': {'TOXICITY': {}}
# }
#
# response = client.comments().analyze(body=analyze_request).execute()
# print(response['attributeScores'])

def get_score(text):
    analyze_request = {
      'comment': { 'text': text },
      'requestedAttributes': {'SEVERE_TOXICITY':{}, 'TOXICITY': {}, 'IDENTITY_ATTACK':{}, 'INSULT':{}, 'PROFANITY':{},
                              'THREAT':{}, 'SEXUALLY_EXPLICIT':{},
                              'SEVERE_TOXICITY_EXPERIMENTAL':{}, 'TOXICITY_EXPERIMENTAL':{},
                              'IDENTITY_ATTACK_EXPERIMENTAL':{}, 'INSULT_EXPERIMENTAL':{}, 'PROFANITY_EXPERIMENTAL':{},
                              'THREAT_EXPERIMENTAL':{}, 'AFFINITY_EXPERIMENTAL':{},'COMPASSION_EXPERIMENTAL':{},
                              'CURIOSITY_EXPERIMENTAL':{}, 'NUANCE_EXPERIMENTAL':{}, 'PERSONAL_STORY_EXPERIMENTAL':{},
                              'REASONING_EXPERIMENTAL' :{}, 'RESPECT_EXPERIMENTAL':{},
                              }
    }
    response = client.comments().analyze(body=analyze_request).execute()
    return response['attributeScores']

# print(get_score("friendly greetings from python"))

def get_score_backoff(text, max_retries=5):
    if text =='':
        print('empty')
        return None
    time.sleep(0.95)
    while max_retries > 0:
        try:
            return get_score(text)
        except HttpError  as e:
            if e.resp.status == 429:
                time.sleep(0.05*2**(6-max_retries))
                print(e)
                max_retries -= 1
            else:
                print(e)

# print(get_toxicity_score_backoff("friendly greetings from python"))

def add_perspective_df(df, count=[0]):
    df['perspective'] = df['text'].apply(get_score)
    count[0] += 1
    print('success '+f"{count[0]}")
    return df

def add_perspective_df_limited(df, count=[0]):
    df['perspective'] = df['text'].apply(get_score_backoff)
    count[0] += 1
    print('success df '+f"{count[0]}")
    return df
