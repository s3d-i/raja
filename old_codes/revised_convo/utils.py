import json
import requests
import pandas as pd
import pickle
import os
from convokit import Corpus
# import spacy
# from collections import Counter

path = "C:/Users/L/.convokit/downloads/"
os.environ['http_proxy'] = 'http://localhost:7890'
os.environ['https_proxy'] = 'http://localhost:7890'
corpusname = path+'conversations-gone-awry-cmv-corpus'

def read_df_list(pickle_file):
    with open(pickle_file, 'rb') as f:
        df_list = pickle.load(f)
    return df_list

def save_df_list(df_list, pickle_file):
    with open(pickle_file, 'wb') as f:
        pickle.dump(df_list, f)
    return

def apply_f_to_df_list(df_list, f):
    return [f(df) for ls in df_list for df in ls]

def flatten_df_list(df_list):
    return [df for ls in df_list for df in ls]

def check_column_type(df):
    r = df.sample(n=1)
    for i in df.columns:
        print(i, type(r[i].values[0]))

def load_dfs_corpus(corpusname):
    corpus = Corpus(filename=corpusname)
    speakers = corpus.get_speakers_dataframe().drop(columns=['vectors'])

    conversations = corpus.get_conversations_dataframe().drop(columns=['vectors'])
    utterances = corpus.get_utterances_dataframe().drop(columns=['vectors'])
    # print(type(speakers), type(conversations), type(utterances))
    return speakers, conversations, utterances


def generate_answer_with_ollama_stream(query='', context='{context not exists}',
                                       system_prompt='You are a helpful assistant',
                                       input_text=None, max_tokens=1, model="llama3:latest",
                                       url="http://localhost:11434/api/generate", top_k=50, top_p=1.0, tem=1.0,
                                       Truecutoff=False, Falsecutoff=False):
    if input_text is not None:
        input = input_text
    else:
        input = f"Question: {query}\nContext: {context}"

    payload = {
        'prompt': input, 'system': system_prompt, 'model': model, 'max_tokens': max_tokens,
        'options': {
            'temperature': tem,
            'top_k': top_k,
            'top_p': top_p,
            # 'seed': 123
        },
    }
    response = requests.post(url, json=payload, stream=True)
    try:
        accumulated_text = ""
        for line in response.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(f"Error in response: {body['error']}")
            if not body.get("done"):
                message = body.get("response", "")
                accumulated_text += message
                # print(accumulated_text)

                if Truecutoff:
                    if "--IMMITATION--" in accumulated_text:
                        return True
                if Falsecutoff:
                    if len(accumulated_text) > 20:
                        return False

            if body.get("done", False):
                return accumulated_text
        return accumulated_text
    except Exception as e:
        print("Failed to decode NDJSON response:", e)
        print("Response content:", response.content)
        raise


def chat_llama_cpp(query='', context='{context not exists}', system_prompt='You are a helpful assistant',
                   input_text=None, max_tokens=1,
                   url="http://localhost:8879/chat/completions", top_k=50, top_p=1.0, tem=1.0, Truecutoff=False,
                   Falsecutoff=False):
    if input_text is not None:
        input = input_text
    else:
        input = f"Question: {query}\nContext: {context}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": input}]
    messages = [
        {"role": "system", "content": system_prompt}]

    data = {
        "messages": messages,
        "prompt": input,
        "system_prompt": system_prompt,
        "stream": True,
        "temperature": tem,
        "max_tokens": max_tokens,
        "top_k": top_k,
        "top_p": top_p,
    }
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data, stream=True)
    # print(response.content.splitlines())

    try:
        accumulated_text = ""
        for line in response.iter_lines():
            # print("########\n")
            if line:
                # print(line)
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:'):
                    json_data = decoded_line[len('data:'):].strip()
                    # print(json_data)
                    try:
                        data = json.loads(json_data)
                        content = data.get('choices')[0].get('delta').get('content')
                        # print(content)
                        if content is not None:

                            accumulated_text += content
                            if Truecutoff:
                                if "--IMMITATION--" in accumulated_text:
                                    return True
                            if Falsecutoff:
                                if len(accumulated_text) > 20:
                                    return False
                        else:
                            return accumulated_text
                        # print(f"Content: {accumulated_text}")
                    except json.JSONDecodeError:
                        print("Failed to decode JSON:", json_data)
    except Exception as e:
        print("Failed to decode NDJSON response:", e)
        print("Response content:", response.content)
        raise


def sentence_immitation_stream(text, top_k=50, top_p=1.0, temperature=1.0, fcutoff=False, tcutoff=False):
    system_prompt = 'OUTPUT FORMAT:\n{"--IMMITATION--": YOUR_IMMITATION_TEXTS}\n\nYour immitation should preserve the Speaker\'s semantic meaning and emotions sentence by sentence.\n'
    input_text = 'Speaker\'s Text:' + f"{text}"
    a = generate_answer_with_ollama_stream(system_prompt=system_prompt, input_text=input_text,
                                           max_tokens=len(text), top_k=top_k, top_p=top_p, tem=temperature,
                                           Falsecutoff=fcutoff, Truecutoff=tcutoff)
    return a


def chat_immitation_stream(text, top_k=50, top_p=1.0, temperature=1.0, fcutoff=False, tcutoff=False):
    system_prompt = 'OUTPUT FORMAT:\n{"--IMMITATION--": YOUR_IMMITATION_TEXTS}\n\nYour immitation should preserve the Speaker\'s semantic meaning and emotions sentence by sentence.\n'
    input_text = 'Speaker\'s Text:' + f"{text}"
    a = chat_llama_cpp(system_prompt=system_prompt, input_text=input_text, max_tokens=len(text), top_k=top_k,
                       top_p=top_p, tem=temperature, Falsecutoff=fcutoff, Truecutoff=tcutoff)
    return a


def complete_llama_cpp(query='', context='{context not exists}', system_prompt='You are a helpful assistant',
                       input_text=None, max_tokens=1,
                       url="http://localhost:8879/completion", top_k=50, top_p=1.0, tem=1.0, Truecutoff=False,
                       Falsecutoff=False):
    if input_text is not None:
        input = input_text
    else:
        input = f"Question: {query}\nContext: {context}"
    data = {
        "prompt": input,
        "system_prompt": system_prompt,
        "stream": True,
        "temperature": tem,
        "max_tokens": max_tokens,
        "top_k": top_k,
        "top_p": top_p,
    }
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)

    try:
        accumulated_text = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:'):
                    json_data = decoded_line[len('data:'):].strip()
                    try:
                        data = json.loads(json_data)
                        content = data.get('content')
                        accumulated_text += content
                        if Truecutoff:
                            if "--IMMITATION--" in accumulated_text:
                                return True
                        if Falsecutoff:
                            if len(accumulated_text) > 20:
                                return False
                        if data.get('stop'):
                            return accumulated_text
                        # print(f"Content: {accumulated_text}")
                    except json.JSONDecodeError:
                        print("Failed to decode JSON:", json_data)
    except Exception as e:
        print("Failed to decode NDJSON response:", e)
        print("Response content:", response.content)
        raise


def completion_immitation_stream(text, top_k=50, top_p=1.0, temperature=1.0, fcutoff=False, tcutoff=False):
    system_prompt = 'OUTPUT FORMAT:\n{"--IMMITATION--": YOUR_IMMITATION_TEXTS}\n\nYour immitation should preserve the Speaker\'s semantic meaning and emotions sentence by sentence.\n'
    input_text = 'Speaker\'s Text:' + f"{text}"
    a = complete_llama_cpp(system_prompt=system_prompt, input_text=input_text, max_tokens=min(len(text), 30),
                           top_k=top_k, top_p=top_p, tem=temperature, Falsecutoff=fcutoff, Truecutoff=tcutoff)
    return a


def check_immitation_successful(combat_df, col_name='imm', signal='--IMMITATION--', possible_signal='": '):
    # check if indicator is True, then format

    def check_imm(x):
        # signal for immitation failure
        return signal in x

    combat_df[col_name + '_check'] = combat_df[col_name].apply(check_imm)
    print(combat_df[col_name + '_check'].values)

    def format_json(x):
        if signal in x:
            result = x.split(signal)[1].split('}')[0]
            if possible_signal in result:
                parts = result.split(possible_signal)
                if len(parts) > 1:
                    return parts[1]
                else:
                    return parts[0]  # or handle the case where possible_signal is at the end
            return result
        return x

    combat_df[col_name] = combat_df.apply(
        lambda row: format_json(row[col_name]) if row[col_name + '_check'] else row['text'], axis=1)

    return combat_df


def get_word_from_tokenid_llamaCpp(id):
    result = requests.post("http://localhost:8879/detokenize", json={"tokens": [id]}).json()
    return result["content"]


def split_text_llamaCpp(text):
    url = "http://localhost:8879/"
    result = requests.post(url + "tokenize", json={"content": text}).json()
    ls = result["tokens"]
    # print(ls)
    return [get_word_from_tokenid_llamaCpp(id) for id in ls]