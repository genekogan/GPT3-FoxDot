import os
import json
import requests
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')



def complete(prompt, 
             stops=None, 
             max_tokens=100, 
             temperature=0.9, 
             engine='davinci',
             max_completions=1):
    
    max_completions = 1 # hard-coded
    n_completions = 0
    n_tokens = 0
    finished = False
    completion = ''

    #print("===========")
    #print("RUN GPT-3")
    #print(prompt)
    while not finished:
        response = openai.Completion.create(
            engine=engine, 
            prompt=prompt, 
            max_tokens=max_tokens, 
            temperature=temperature,
            stop=stops)
        
        n_completions += 1
        text = response.choices[0].text
        completion += text
        prompt += text
        #n_tokens = count_tokens(prompt)
        finished = True
        #finished = (response.choices[0].finish_reason == 'stop') \
        #    or (n_completions >= max_completions) \
        #    or (n_tokens + max_tokens >= 2000)  # maximum token limit
    
    # print("===========")
    # print("COMPLETION")
    # print(completion)
    # print("===========")
    return completion.strip()


def search(documents, query, engine='davinci'):
    data = json.dumps({"documents": documents, "query": query})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % os.getenv('OPENAI_API_KEY'),
    }
    response = requests.post('https://api.openai.com/v1/engines/{}/search'.format(engine), headers=headers, data=data)
    result = json.loads(response.text)
    return result
