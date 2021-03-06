import json
import pickle
import random
import re

import numpy as np
from pythainlp import word_tokenize
from tensorflow import keras
import tensorflow as tf

from chatbot.find_data import find
from chatbot.recommend import recommend


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)


model = keras.models.load_model("model_and_data/model")

with open("model_and_data/data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)

with open("knowledge_base/intents.json", "r", encoding="utf-8") as f:
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
    if re.match(r"[a-z0-9-:()_\[\]'!&.]+", inp):
        keep_word = ['hi', "hello", "bye", "thank", "spec", "singleplayer", "multiplayer", "link", "random"]
        words = re.findall(r"[a-z0-9-:()_\[\]'!&.]+", inp_to_predict)
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


def chat(inp):
    inp_to_predict = clean_input(inp)

    results = model.predict(bag_of_words(inp_to_predict))
    results_index = np.argmax(results)
    tag = labels[results_index]
    print(results[0][results_index])
    if results[0][results_index] > 0.8:
        return get_response(tag, inp)

    responses = data['fail']["dontknow"]
    response = random.choice(responses)
    return response
