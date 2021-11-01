from pathlib import Path
import pickle

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from matplotlib import pyplot as plt


def training_model():
    data_path = Path("app/model_and_data/data.pickle")
    model_path = Path("app/model_and_data/model")

    with open(data_path, "rb") as f:
        words, labels, training, output = pickle.load(f)

    tf.compat.v1.reset_default_graph()

    # define the keras model
    model = Sequential()
    model.add(Dense(8, activation="relu", input_shape=(len(training[0]),)))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(len(output[0]), activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    # model.fit(training, output, epochs=250, batch_size=8)

    history = model.fit(training, output, epochs=110, batch_size=8)

    # accuracy and epoch
    plt.plot(history.history["accuracy"])
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.show()

    # loss and epoc
    plt.plot(history.history["loss"])
    plt.title("model loss")
    plt.ylabel("loss")
    plt.xlabel("epoch")
    plt.show()

    model.save(model_path)
