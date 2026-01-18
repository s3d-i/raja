import spacy
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.sparse import csr_matrix, issparse

nlp = spacy.load('en_core_web_sm')


def preprocess_text_lemmatize(text, stop_words=['he']):
    doc = nlp(text)

    lemmatized_words = []

    for token in doc:
        if not token.is_stop and token.is_alpha and token.text.lower() not in stop_words:
            lemmatized_words.append(token.lemma_)

    return ' '.join(lemmatized_words)

def get_tf_idf_sparse_matrix(texts):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    return X

def get_count_sparse_matrix(texts):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    return X

def filter_threshold(matrix, threshold=0.1):
    if issparse(matrix):
        filtered_matrix = matrix.copy()
        filtered_matrix.data[filtered_matrix.data < threshold] = 0
        filtered_matrix.eliminate_zeros()
    else:
        filtered_matrix = matrix.copy()
        filtered_matrix[filtered_matrix < threshold] = 0
    return filtered_matrix

def filter_threshold_percent(X, p = 0.9):
    non_zero_counts = np.array((X != 0).sum(axis=0)).flatten()
    threshold = p * X.shape[0]
    columns_to_keep = np.where(non_zero_counts <= threshold)[0]
    X_filtered = X[:, columns_to_keep]
    return X_filtered

def WoB_from_token_list(tkls):
    word_freq = Counter(tkls)
    sorted_word_freq = dict(word_freq.most_common())
    return sorted_word_freq

def merge_word_bag_list(word_bag_list):
    merged_word_bag = {}
    for word_bag in word_bag_list:
        for word, freq in word_bag.items():
            if word in merged_word_bag:
                merged_word_bag[word] += freq
            else:
                merged_word_bag[word] = freq
    return merged_word_bag

# stop_words = ['he']
# texts = ["He is running faster than his friend. She enjoys playing football, and they both love running.", "I love playing tennis, and I enjoy making love. He fucks me every night."]
# processed = [preprocess_text_lemmatize(text, stop_words=stop_words) for text in texts]
#
# print("Word Bag:", processed)
# print(get_tf_idf_sparse_matrix(texts))