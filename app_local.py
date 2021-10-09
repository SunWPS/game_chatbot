import json
from pathlib import Path
import pickle
import random
import os
import re

import numpy as np
from pythainlp import word_tokenize
from tensorflow import keras

from app.find_data import find
from app.recommend import recommend

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
    inp_to_predict = inp.lower().replace(" ", "")
    if re.match(r"[a-z0-9-:()\[\]®'!™&.]+", inp):
        keep_word = ['hi', "hello", "bye", "thank", "spec", "singleplayer", "multiplayer", "url"]
        words = re.findall(r"[a-z0-9-:()\[\]®'!™&.]+", inp_to_predict)
        for word in words:
            if word not in keep_word:
                inp_to_predict = inp_to_predict.replace(word, "")
    return inp_to_predict


def get_response(tag, inp):
    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
            response = random.choice(responses)
            if re.match(r"^get", tag):
                response = find(tag, response, inp)
            elif re.match(r"^recommend", tag):
                response = recommend(tag, response, inp)
            break
    return response


def chat():
    print("เริ่มพูดกับ bot")
    while True:
        inp = input("You: ")

        inp_to_predict = clean_input(inp)

        results = model.predict(bag_of_words(inp_to_predict))
        results_index = np.argmax(results)
        tag = labels[results_index]

        if results[0][results_index] > 0.7:
            print(get_response(tag, inp))

            if tag == "end_conversation":
                break
        else:
            print("ชอโทษครับ ผมไม่เข้าใจครับ")


chat()