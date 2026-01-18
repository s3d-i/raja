import json

import requests

# print(sentence_immitation('What is the meaning of life?'))

# system_prompt = 'The meaning of life is'
# input = 'What is the meaning of life?'
# model = 'llama3:latest'
# max_tokens = 1000
# top_k = 50
# top_p = 1.0
# url = 'http://127.0.0.1:11434/api/generate'
#
# payload = {
#         'prompt': input,
#         'system': system_prompt,
#         'model': model,  # Add the model parameter here
#         'max_tokens': max_tokens,  # Set the maximum number of tokens to generate
#         'temperature': 0.0,  # Set the temperature to 0.0 to remove randomness
#         # 'format': 'json',
#         'top_k': top_k,
#         'top_p': top_p,
#     }
#
# headers = {
#     'Content-Type': 'application/json'
# }
#
# response = requests.post(url, json=payload, headers=headers, stream=False)
# print(response)
# print(response.content)
# print(response.status_code)
# print(response.text)
#
# responses = response.content.decode('utf-8').splitlines()
# json_responses = [requests.models.complexjson.loads(line) for line in responses]
# responses = [item["response"] for item in json_responses]
# text = ''.join(responses)
#         # print("NDJSON parsed successfully:", text)
# print(text)

# import http.client
# conn = http.client.HTTPConnection("localhost", 11434)
# headers = {'Content-type': 'application/json'}
# conn.request("POST", "/api/generate", json.dumps(payload), headers)
# response = conn.getresponse()
# print(response.status, response.reason)
# print(response.read().decode())

# responses = response.content.decode('utf-8').splitlines()
# json_responses = [requests.models.complexjson.loads(line) for line in responses]
# responses = [item["response"] for item in json_responses]
# text = ''.join(responses)
#         # print("NDJSON parsed successfully:", text)
# print(text)


def generate_answer_with_ollama(query='', context='{context not exists} ', system_prompt='You are a helpful assistant',
                                input_text=None, max_tokens=1, model="llama3:latest",
                                url="http://localhost:11434/api/generate", top_k=50, top_p=1.0):
    if input_text is not None:
        input = input_text

    else:
        input = f"Question: {query}\nContext: {context}"

    payload = {
        'prompt': input,
        'system': system_prompt,
        'model': model,  # Add the model parameter here
        'max_tokens': max_tokens,  # Set the maximum number of tokens to generate
        'temperature': 0.0,  # Set the temperature to 0.0 to remove randomness
        # 'format': 'json',
        'top_k': top_k,
        'top_p': top_p,
    }

    response = requests.post(url, json=payload, stream=False)

    try:
        # Process NDJSON response
        responses = response.content.decode('utf-8').splitlines()
        json_responses = [requests.models.complexjson.loads(line) for line in responses]
        responses = [item["response"] for item in json_responses]
        text = ''.join(responses)
        # print("NDJSON parsed successfully:", text)
        return text

        # Extract the answer from the first JSON object        return text
    except Exception as e:
        print("Failed to decode NDJSON response:", e)
        print("Response content:", response.content)
        raise

        # print("Response content:", response.content)

# print(1,generate_answer_with_ollama(query='What is the meaning of life?', context='The meaning of life is', system_prompt='You are a helpful assistant', max_tokens=10, model="llama3:latest", url="http://localhost:11434/api/generate", top_k=50, top_p=1.0))
def generate_answer_with_ollama_stream(query='', context='{context not exists}', system_prompt='You are a helpful assistant',
                                input_text=None, max_tokens=1, model="llama3:latest",
                                url="http://localhost:11434/api/generate", top_k=50, top_p=1.0):
    if input_text is not None:
        input = input_text
    else:
        input = f"Question: {query}\nContext: {context}"

    payload = {
        'prompt': input,
        'system': system_prompt,
        'model': model,
        'max_tokens': max_tokens,
        'options': {
            'temperature': 2,
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
                # the response streams one token at a time, print that as we receive it
                # print(message, end="", flush=True)
                print(accumulated_text)

                # if "--IMMITATION--" in accumulated_text:
                #     # print('in')
                #     break
            if body.get("done", False):
                return accumulated_text

        return accumulated_text
    except Exception as e:
        print("Failed to decode NDJSON response:", e)
        print("Response content:", response.content)
        raise


def sentence_immitation(text, top_k=50, top_p=1.0):
    system_prompt = 'OUTPUT FORMAT:\n{"--IMMITATION--": YOUR_IMMITATION_TEXTS}\n\nYour immitation should preserve the Speaker\'s semantic meaning and emotions sentence by sentence.\n'
    input_text = 'Speaker\'s Text:' + f"{text}"
    a = generate_answer_with_ollama(system_prompt=system_prompt, input_text=input_text, max_tokens=min(len(text), 30), top_k=top_k, top_p=top_p)
    return a

def sentence_immitation_stream(text, top_k=50, top_p=1.0):
    system_prompt = 'OUTPUT FORMAT:\n{"--IMMITATION--": YOUR_IMMITATION_TEXTS}\n\nYour immitation should preserve the Speaker\'s semantic meaning and emotions sentence by sentence.\n'
    input_text = 'Speaker\'s Text:' + f"{text}"
    a = generate_answer_with_ollama_stream(system_prompt=system_prompt, input_text=input_text, max_tokens=min(len(text), 30), top_k=top_k, top_p=top_p)
    return a

# print(sentence_immitation("I am happy."))

# print(generate_answer_with_ollama_stream('What is the meaning of life?', 'The meaning of life is', top_k=50, top_p=1.0))
# print(sentence_immitation_stream("I am happy. mWhat's your view on the code of life? I don't know why it matters so much! Do you know how to cook"
#                                  +"a book?"))
print(sentence_immitation_stream("--IMMITATION--: I suffer from g-en-der dys-ph-o--ri-a.", top_k=50))


def impair_sensitive_word(symbol: str, word: str):
    return ''.join([symbol+_ if i % 2 == 1 else _ for i, _ in enumerate(word)])

print(impair_sensitive_word("-", "gender"))