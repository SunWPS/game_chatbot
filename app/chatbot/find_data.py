import re
import random
import json
import configparser

import mysql.connector
from mysql.connector.constants import ClientFlag


with open("knowledge_base/intents.json", "r", encoding="utf-8") as f:
    fail = json.load(f)

config = configparser.ConfigParser()
config.read('Configuration.ini')

config = {
    'user': config['database']['user'],
    'password': config['database']['password'],
    'host': config['database']['host'],
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': "ssl/server-ca.pem",
    'ssl_cert': "ssl/client-cert.pem",
    'ssl_key': "ssl/client-key.pem",
    'database': config['database']['database']
}


def get_information(data):
    return "\n" + data.strip()


def get_price(price):
    if price == 0:
        return "ฟรีครับ"
    return " ราคา " + str(price) + " บาทครับ"


def get_language(languages):
    return re.sub(r",", ", ", languages.strip())


def get_minimum_spec(spec):
    return "\n"+"\n".join(spec.strip().split(","))


def get_singleplayer(single):
    return "มีโหมด Single Player ครับ" if single == 1 else "ไม่มีโหมด Single Player ครับ"


def get_multiplayer(multi):
    return "มีโหมด Multi Player ครับ" if multi == 1 else "ไม่มีโหมด Multi Player ครับ"


def get_thai(thai):
    return "รองรับภาษาไทยครับ" if thai == 1 else "ไม่รองรับภาษาไทยครับ"


def get_developer(developer):
    return developer.strip() + " ครับ"


def get_release_year(year):
    return str(year) + " ครับ"


def get_url(url):
    return url.strip() + " ครับ"


def get_genre(genre):
    return genre.replace(",", ", ") + " ครับ"


def get_review(game, cursor):
    percent = normal_query(game, "positive_percent", cursor)
    user = normal_query(game, "user_review", cursor)
    return str(percent) + "% จากการรีวิวทั้งหมด " + str(user) + " คน"


def get_game_mode(game, cursor):
    sp = normal_query(game, "single_player", cursor)
    mp = normal_query(game, "multi_player", cursor)

    if not sp or not mp:
        return False
    elif sp == 1 and mp == 1:
        return "Single Player และ Multi Player ครับ"
    elif sp == 1:
        return "แค่ Single Player ครับ"
    else:
        return "แค่ Multi Player ครับ"


def get_is_free(game, cursor):
    price = normal_query(game, "price", cursor)
    if price == 0:
        return "ฟรีครับ"
    else:
        return "ไม่ฟรีครับ" + " ราคา " + str(price) + " บาทครับ"


def normal_query(game, column, cursor):
    query = "select " + column + ' from gamesdata where lower(name) = "' + game.lower() + '";'
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    return data[0][0]


def query_data(game, column, function, cursor):
    query = "select " + column + ' from gamesdata where lower(name) = "' + game.lower() + '";'
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    return function(data[0][0])


def find_game(inp):
    keep_word = ["spec", "singleplayer", "multiplayer", "link", "single", "multi", "player", "random"]
    words = re.findall(r"[A-Za-z0-9-:()_\[\]'!&.]+", inp)
    return " ".join([i for i in words if i.lower() not in keep_word])


def find(tag, response, inp):
    function_dict = {"get_information": [get_information, "desc_snippet"],
                     "get_price": [get_price, "price"],
                     "get_language": [get_language, "languages"],
                     "get_minimum_spec": [get_minimum_spec, "minimum_requirements"],
                     "get_singleplayer": [get_singleplayer, "single_player"],
                     "get_multiplayer": [get_multiplayer, "multi_player"],
                     "get_thai": [get_thai, "thai"],
                     "get_developer": [get_developer, "developer"],
                     "get_release_year": [get_release_year, "release_date"],
                     "get_url": [get_url, "url"],
                     "get_genre": [get_genre, "genre"]}

    extra_dict = {"get_review": get_review,
                  "get_game_mode": get_game_mode,
                  "get_is_free": get_is_free}

    game = find_game(inp)
    if game == "":
        responses = fail['fail']["cantfindgame"]
        response = random.choice(responses)
        return response

    cncx = mysql.connector.connect(**config)
    cursor = cncx.cursor()

    if tag not in extra_dict:
        txt = query_data(game, function_dict[tag][1], function_dict[tag][0], cursor)
    else:
        txt = extra_dict[tag](game, cursor)

    cncx.close()

    if not txt:
        responses = fail['fail']["donthavedata"]
        response = random.choice(responses)
        return response.replace("{game}", game)

    return (response + txt).replace("{game}", game)
