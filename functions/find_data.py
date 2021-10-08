import re
import pickle
from pathlib import Path

import pandas as pd


games_path = Path("data/games.pickle")

with open(games_path, "rb") as f:
    df, genre, language, tags = pickle.load(f)
    
pd.set_option('display.max_colwidth', None)


def get_infomation(game):
    return df[df["name"].str.lower() == game.lower()]["desc_snippet"].to_string(index=False).strip()


def get_price(game):
    return df[df["name"].str.lower() == game.lower()]["price"].to_string(index=False).strip() + " บาท"


def get_language(game):
    return re.sub(r",", ", ", df[df["name"].str.lower() == game.lower()]["languages"].to_string(index=False).strip())


def get_minimun_spec(game):
    txt = df[df["name"].str.lower() == game.lower()]["minimum_requirements"].to_string(index=False)
    return "\n".join(txt.strip().split(","))


def game_mode(game):
    sp = int(df[df["name"].str.lower() == game.lower()]["single_player"].to_string(index=False))
    mp = int(df[df["name"].str.lower() == game.lower()]["multi_player"].to_string(index=False))
    if(sp == 1 and mp == 1):
      return "Single Player และ Multi Player ครับ"
    elif(sp == 1):
      return "แค่ Single Player ครับ"
    else:
      return "แค่ Multi Player ครับ"


def get_singleplayer(game):
    return "มีครับ" if int(df[df["name"].str.lower() == game.lower()]["single_player"].to_string(index=False)) == 1 else "ไม่มีครับ"


def get_multiplayer(game):
    return "มีครับ" if int(df[df["name"].str.lower() == game.lower()]["multi_player"].to_string(index=False)) == 1 else "ไม่มีครับ"


def get_thai(game):
    return "มีครับ" if int(df[df["name"].str.lower() == game.lower()]["thai"].to_string(index=False)) == 1 else "ไม่มีครับ"


def is_free(game):
  data = get_price(game)
  if data == 0:
    return "ฟรีครับ"
  else:
    return "ไม่ฟรีครับ" +  "ราคา " + str(data)


def get_developer(game):
    return df[df["name"].str.lower() == game.lower()]["developer"].to_string(index=False).strip()


def get_release_year(game):
    return df[df["name"].str.lower() == game.lower()]["release_date"].to_string(index=False).strip()


def get_url(game):
    return df[df["name"].str.lower() == game.lower()]["url"].to_string(index=False).strip()


def get_review(game):
    percent = df[df["name"].str.lower() == game.lower()]["positive_percent"].to_string(index=False).strip()
    user = df[df["name"].str.lower() == game.lower()]["user_review"].to_string(index=False).strip()
    return percent + "% จากการรีวิวทั้งหมด " + user + " คน"


def get_tag(game):
    return re.sub(r",", ", ", df[df["name"].str.lower() == game.lower()]["popular_tags"].to_string(index=False).strip())


def find_game(inp):
    # if don't have game
    keep_word = ["spec", "singleplayer", "multiplayer", "url", "single", "multi", "player"]
    words = re.findall(r"[A-Za-z-']+", inp)
    return " ".join([i for i in words if i.lower() not in keep_word])
            

def find(tag, response, inp):
    function_dict = {"get_infomation": get_infomation,
                    "get_price" : get_price,
                    "get_language": get_language,
                    "get_minimun_spec": get_minimun_spec,
                    "get_game_mode": game_mode,
                    "get_singleplayer": get_singleplayer,
                    "get_multiplayer": get_multiplayer,
                    "get_thai": get_thai,
                    "get_is_free": is_free,
                    "get_developer": get_developer,
                    "get_release_year": get_release_year,
                    "get_url": get_url,
                    "get_review": get_review,
                    "get_tag": get_tag}
    
    game = find_game(inp)
    
    return (response + function_dict[tag](game)).replace("{game}", game)

# print(find("get_singleplayer", "", "DOOM มีโหมด single player หรือไม่"))