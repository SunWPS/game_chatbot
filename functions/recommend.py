import re
import pickle
from pathlib import Path

import pandas as pd


games_path = Path("data/games.pickle")

with open(games_path, "rb") as f:
    df, genre, language, tags = pickle.load(f)
    
pd.set_option('display.max_colwidth', None)


def recommend_single_player():
  i = 1
  txt = ""
  for name in df[df["single_player"] == 1].sort_values("wavg", ascending=False)["name"].head():
    txt += str(i) + ". " + name + "\n"
    i += 1
  return(txt)


def recommend_multi_player():
  i = 1
  txt = ""
  for name in df[df["multi_player"] == 1].sort_values("wavg", ascending=False)["name"].head():
    txt += str(i) + ". " + name + "\n"
    i += 1
  return(txt)


def recommend_free():
  i = 1
  txt = ""
  for name in df[df["price"] == 0].sort_values("wavg", ascending=False)["name"].head():
    txt += str(i) + ". " + name + "\n"
    i += 1
  return(txt)


def recommed_morethan_year(inp):
  year = int(re.findall(r"\d\d\d\d", inp)[0])
  i = 1
  txt = ""
  for name in df[df["release_date"].astype('int64') > year].sort_values("wavg", ascending=False)["name"].head():
    txt += str(i) + ". " + name + "\n"
    i += 1
  return txt
    

def recommed_lessthan_year(inp):
  year = int(re.findall(r"\d\d\d\d", inp)[0])
  i = 1
  txt = ""
  for name in df[df["release_date"].astype('int64') < year].sort_values("wavg", ascending=False)["name"].head():
    txt += str(i) + ". " + name + "\n"
    i += 1
  return txt


def recommed_in_year(inp):
  year = int(re.findall(r"\d\d\d\d", inp)[0])
  i = 1
  txt = ""
  for name in df[df["release_date"].astype('int64') == year].sort_values("wavg", ascending=False)["name"].head():
    txt += str(i) + ". " + name + "\n"
    i += 1
  return txt


def recommed_morethan_price(inp):
  price = int(re.findall(r"\d+", inp)[0])
  i = 1
  txt = ""
  for name in df[df["price"] > price].sort_values("wavg", ascending=False)["name"].head():
    txt += str(i) + ". " + name + "\n"
    i += 1
  return txt


def recommed_lessthan_price(inp):
  price = int(re.findall(r"\d+", inp)[0])
  i = 1
  txt = ""
  for name in df[df["price"] < price].sort_values("wavg", ascending=False)["name"].head():
    txt += str(i) + ". " + name + "\n"
    i += 1
  return txt
