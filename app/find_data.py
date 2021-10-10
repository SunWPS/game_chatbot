import re
import random
import pickle
import json
from pathlib import Path

import pandas as pd


games_path = Path("data/games.pickle")
intents_path = Path("intents.json")

with open(games_path, "rb") as f:
    df, genre, language, tags = pickle.load(f)

with open(intents_path, "r", encoding="utf-8") as f:
    fail = json.load(f)

pd.set_option('display.max_colwidth', None)


def get_information(game):
    return "\n" + df[df["name"].str.lower() == game.lower()]["desc_snippet"].to_string(index=False).strip()


def get_price(game):
    price = df[df["name"].str.lower() == game.lower()]["price"].to_string(index=False).strip()
    if int(price) == 0:
        return "ฟรีครับ"
    return " ราคา " + price + " บาทครับ"


def get_language(game):
    return re.sub(r",", ", ", df[df["name"].str.lower() == game.lower()]["languages"].to_string(index=False).strip())


def get_minimum_spec(game):
    txt = df[df["name"].str.lower() == game.lower()]["minimum_requirements"].to_string(index=False)
    return "\n"+"\n".join(txt.strip().split(","))


def get_game_mode(game):
    sp = int(df[df["name"].str.lower() == game.lower()]["single_player"].to_string(index=False))
    mp = int(df[df["name"].str.lower() == game.lower()]["multi_player"].to_string(index=False))
    if sp == 1 and mp == 1:
        return "Single Player และ Multi Player ครับ"
    elif sp == 1:
        return "แค่ Single Player ครับ"
    else:
        return "แค่ Multi Player ครับ"


def get_singleplayer(game):
    return "มีโหมด Single Player ครับ" if int(
        df[df["name"].str.lower() == game.lower()]["single_player"].to_string(index=False)) == 1 \
        else "ไม่มีโหมด Single Player ครับ"


def get_multiplayer(game):
    return "มีโหมด Multi Player ครับ" if int(
        df[df["name"].str.lower() == game.lower()]["multi_player"].to_string(index=False)) == 1 \
        else "ไม่มีโหมด Multi Player ครับ"


def get_thai(game):
    return "รองรับภาษาไทยครับ" if int(
        df[df["name"].str.lower() == game.lower()]["thai"].to_string(index=False)) == 1 else "ไม่รองรับภาษาไทยครับ"


def get_is_free(game):
    data = get_price(game)
    if data == "ฟรีครับ":
        return "ฟรีครับ"
    else:
        return "ไม่ฟรีครับ" + str(data)


def get_developer(game):
    return df[df["name"].str.lower() == game.lower()]["developer"].to_string(index=False).strip() + " ครับ"


def get_release_year(game):
    return df[df["name"].str.lower() == game.lower()]["release_date"].to_string(index=False).strip() + " ครับ"


def get_url(game):
    return df[df["name"].str.lower() == game.lower()]["url"].to_string(index=False).strip() + " ครับ"


def get_review(game):
    percent = df[df["name"].str.lower() == game.lower()]["positive_percent"].to_string(index=False).strip()
    user = df[df["name"].str.lower() == game.lower()]["user_review"].to_string(index=False).strip()
    return percent + "% จากการรีวิวทั้งหมด " + user + " คน"


def get_tag(game):
    return re.sub(r",", ", ", df[df["name"].str.lower() == game.lower()]["popular_tags"].to_string(index=False).strip())


def find_game(inp):
    keep_word = ["spec", "singleplayer", "multiplayer", "link", "single", "multi", "player"]
    words = re.findall(r"[A-Za-z0-9-:()_\[\]'!&.]+", inp)
    print(words)
    return " ".join([i for i in words if i.lower() not in keep_word])


def find(tag, response, inp):
    function_dict = {"get_information": get_information,
                     "get_price": get_price,
                     "get_language": get_language,
                     "get_minimum_spec": get_minimum_spec,
                     "get_game_mode": get_game_mode,
                     "get_singleplayer": get_singleplayer,
                     "get_multiplayer": get_multiplayer,
                     "get_thai": get_thai,
                     "get_is_free": get_is_free,
                     "get_developer": get_developer,
                     "get_release_year": get_release_year,
                     "get_url": get_url,
                     "get_review": get_review,
                     "get_tag": get_tag}

    game = find_game(inp)
    if game == "":
        responses = fail['fail']["cantfindgame"]
        response = random.choice(responses)
        return response

    txt = function_dict[tag](game)
    if "Series([], )" in txt:
        responses = fail['fail']["donthavedata"]
        response = random.choice(responses)
        return response.replace("{game}", game)

    return (response + txt).replace("{game}", game)
