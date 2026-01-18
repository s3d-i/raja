import os, pandas as pd
from convokit import Corpus, Speaker, Utterance, Conversation, download


path = "C:/Users/L/.convokit/downloads/"
os.environ['http_proxy'] = 'http://localhost:7890'
os.environ['https_proxy'] = 'http://localhost:7890'
# def get_corpus_name_list(path):
#     corpus_name_list = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
#     print(corpus_name_list)
#     return corpus_name_list
#
# get_corpus_name_list(path)

def load_dfs(corpus):
    speakers = corpus.get_speakers_dataframe()
    conversations = corpus.get_conversations_dataframe()
    utterances = corpus.get_utterances_dataframe()
    # print(type(speakers), type(conversations), type(utterances))
    return speakers, conversations, utterances

def print_overview(speaker_df, convo_df, utt_df,corpus_name=None):
    print("UttDf attributes:", list(utt_df.columns),'\n')
    print("ConvDf attributes:", list(convo_df.columns),'\n')
    print("SpeakerDf attributes:", list(speaker_df.columns),'\n')

    print(convo_df.sample(n=2))
    print(convo_df.shape)

    print(speaker_df.sample(n=2))
    print(speaker_df.shape)

    print(utt_df.sample(n=2))
    print(utt_df.shape)

list1 = ['conversations-gone-awry-cmv-corpus', 'subreddit-ADD', 'subreddit-AmericanPolitics', 'subreddit-Cornell', 'subreddit-NSFW_Social', 'subreddit-POLUG3']
for i in list1:
    corpus = Corpus(filename=path+i)
    print(corpus)
    speakers, conversations, utterances = load_dfs(corpus)
    print_overview(speakers, conversations, utterances,corpus_name=i)
    print("#############################################")