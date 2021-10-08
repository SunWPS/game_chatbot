import json
from pathlib import Path
import pickle
import random
import os
import re

import numpy as np
from pythainlp import word_tokenize
from tensorflow import keras

from functions.find_data import find


# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

model_path = Path("prepare/model")
data_path = Path("prepare/data.pickle")
intents_path = Path("intents.json")

model = keras.models.load_model(model_path)

with open(data_path, "rb") as f:
    words, labels, training, output = pickle.load(f)
    
    
with open(intents_path, "r", encoding="utf-8") as f:
    data = json.load(f)


def bag_of_words(s):
    bag = [0 for _ in range(len(words))]
    
    s_words = word_tokenize(s, engine="deepcut")
    
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array([bag])

def clean_input(inp):
    inp_topredict = inp.lower().replace(" ", "")
    if re.match(r"[a-z-']+", inp):
        keep_word = ['hi', "hello", "bye", "thank", "spec", "singleplayer", "multiplayer", "url"]
        words = re.findall(r"[a-z-']+", inp_topredict)
        for word in words:
            if word not in keep_word:
                inp_topredict = inp_topredict.replace(word, "")
    return inp_topredict
    

def get_ressponse(tag, inp):
    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
            response = random.choice(responses)
            if re.match(r"^get", tag):
                response = find(tag, response, inp)
            break    
    return response
              
    
def chat():
    print("เริ่มพูดกับ bot")
    while True:
        inp = input("You: ")
        
        inp_topredict = clean_input(inp)
        
        results = model.predict(bag_of_words(inp_topredict))
        results_index = np.argmax(results)
        tag = labels[results_index]
        
        if results[0][results_index] > 0.7:
            print(get_ressponse(tag, inp))
            
            if tag == "end_conversation":
                break
        else:
            print("try again")
            
chat()
