from convokit import Corpus, download

corpus = Corpus(filename=download("subreddit-Cornell"))
corpus.print_summary_stats()

for convo in list(corpus.iter_conversations())[:3]:
    print(convo)


corpus = Corpus(filename=download("subreddit-POLUG3"))
corpus.print_summary_stats()

for convo in list(corpus.iter_conversations())[:3]:
    print(convo)