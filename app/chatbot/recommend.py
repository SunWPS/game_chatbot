import re

import mysql.connector
from mysql.connector.constants import ClientFlag


config = {
    'user': '',
    'password': '',
    'host': '',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': "ssl/server-ca.pem",
    'ssl_cert': "ssl/client-cert.pem",
    'ssl_key': "ssl/client-key.pem",
    'database': ''
}


def query_data(inp_query, cursor):
    query = "select name from gamesdata " + inp_query + ";"
    cursor.execute(query)
    return cursor.fetchall()


def where_and_random(column, command, value, cursor):
    games = query_data("where " + column + command + str(value) + " order by wavg DESC  limit 5", cursor)
    i = 1
    txt = ""
    for name in games:
        txt += str(i) + ". " + name[0] + "\n"
        i += 1
    return txt


def recommend_random(cursor):
    games = query_data("order by rand() limit 5", cursor)
    i = 1
    txt = ""
    for name in games:
        txt += str(i) + ". " + name[0] + "\n"
        i += 1
    return txt


def recommend_single_player(cursor):
    return where_and_random("single_player", "=", 1, cursor)


def recommend_multi_player(cursor):
    return where_and_random("multi_player", "=", 1, cursor)


def recommend_free(cursor):
    return where_and_random("price", "=", 0, cursor)


def recommend_morethan_year(inp, cursor):
    year = re.findall(r"\d\d\d\d", inp)[0]
    txt = where_and_random("release_date", ">", year, cursor)
    return year, txt;


def recommend_lessthan_year(inp, cursor):
    year = re.findall(r"\d\d\d\d", inp)[0]
    txt = where_and_random("release_date", "<", year, cursor)
    return year, txt;


def recommend_in_year(inp, cursor):
    year = re.findall(r"\d\d\d\d", inp)[0]
    txt = where_and_random("release_date", "=", year, cursor)
    return year, txt;


def recommend_morethan_price(inp, cursor):
    price = re.findall(r"\d+", inp)[0]
    txt = where_and_random("price", ">", price, cursor)
    return price, txt;


def recommend_lessthan_price(inp, cursor):
    price = re.findall(r"\d+", inp)[0]
    txt = where_and_random("price", "<", price, cursor)
    return price, txt;


def recommend(tag, response, inp):
    no_argm = {"recommend_random": recommend_random,
               "recommend_single_player": recommend_single_player,
               "recommend_multi_player": recommend_multi_player,
               "recommend_free": recommend_free, }
    have_argm = {"recommend_morethan_year": recommend_morethan_year,
                 "recommend_lessthan_year": recommend_lessthan_year,
                 "recommend_in_year": recommend_in_year,
                 "recommend_morethan_price": recommend_morethan_price,
                 "recommend_lessthan_price": recommend_lessthan_price, }

    cncx = mysql.connector.connect(**config)
    cursor = cncx.cursor()

    if tag in no_argm:
        txt = response + "\n" + no_argm[tag](cursor)
    else:
        data, txt = have_argm[tag](inp, cursor)
        txt = (response + "\n" + txt).replace("{data}", data)

    cursor.close()
    return txt
