# Game Chatbot

This is a project for my Natural Language Processing (NLP) class that aims to improve my knowledge of Deep learning
and NLP base on Thai language.

## The Data Set
https://www.kaggle.com/trolukovich/steam-games-complete-dataset

## Used Tools
My Intents Classification was built with Keras, and I deployed my chatbot on Google Cloud Platform.

## Design and Development
###  System Architecture
Chatbot takes messages and converts text to vector data. Then send the data to the intents classification model. Finally, take the tag of the input to find the response messages from the knowledge base.

<p align="center">
    <img widht="460" height="300" src="https://github.com/SunWPS/game_chatbot/blob/master/picture/system.jpg?raw=true">
</p>

## Intents Classification Model
<p align="center">
    <img widht="460" height="300" src="https://github.com/SunWPS/game_chatbot/blob/master/picture/dnn.jpg?raw=true">
</p>

## Deploy
For using my chatbot with Line, I used Cloud Run to deploy my chatbot and Cloud SQL to deploy my database.
<p align="center">
    <img widht="230" height="150" src="https://github.com/SunWPS/game_chatbot/blob/master/picture/deploy.jpg?raw=true">
</p>

For the local
1. Create the Intents classification model by running training.py in the prepare_model folder.
```
python .\prepare_model\training.py
```
2. Create a Docker image and run a container.
```
docker build -t <image-name> .
docker run --name <container_name> -p <local_port>:80 <image-name>
```

## Follow Me On
[Linkedin: Wongsakorn Pinvasee](https://www.linkedin.com/in/wongsakorn-pinvasee-b57b34186/)


