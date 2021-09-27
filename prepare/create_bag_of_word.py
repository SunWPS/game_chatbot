import json
from pathlib import Path
import pickle

import numpy as np
from pythainlp import word_tokenize

def create_bag_of_word():
    intents_path = Path("intents.json")
    pickle_path = Path("prepare/data.pickle")

    with open(intents_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            tokens = word_tokenize(pattern, engine="deepcut")
            words.extend(tokens)
            docs_x.append(tokens)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])
            
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        for w in words:
            if w in doc:
                bag.append(1)
            else:
                bag.append(0)
        
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open(pickle_path, "wb") as f:
        pickle.dump((words, labels, training, output), f)
        