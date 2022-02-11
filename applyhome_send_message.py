from playwright.sync_api import Playwright, sync_playwright
import time
import random

import os
from pathlib import Path

import datetime

import logging
import logging.config
import json

import platform

import csv

import telegram

from urllib.parse import unquote, quote, quote_plus, urlencode

import sys

import credential

def __getLogger():
  with open("./logging.json", "rt") as file:
    config = json.load(file)
  
  logging.config.dictConfig(config)
  
  return logging.getLogger()

#텔레그램봇으로 전송
def sendTgBot(text):
  bot = telegram.Bot(token=credential.CHAT_TOKEN)
  bot.sendMessage(chat_id=credential.CHAT_ID, text=text, parse_mode="markdown")

def main(date):
  with open('applyhome.json', 'r', encoding="utf-8") as file:
    applyhome = json.load(file)

    try:
      list = applyhome[date[0]]

      for el in list:
        naver_parsed_url = "https://m.map.naver.com/search2/search.naver?query=%s&sm=hty&style=v5#/search" % quote(el['addr'])
        google_pared_url = "https://www.google.com/maps/place/%s" % quote(el['addr'])

        sendTgBot("**%s %s 청약 일정**\n\n[%s - %s]\n[%s](%s)\n\n[네이버 지도로 보기](%s)\n[구글 지도로 보기](%s)" % (date[1], date[0], el['type'], el['short_addr'], el['name'], el['link'], naver_parsed_url, google_pared_url))
    except Exception as e:
      sendTgBot("**%s %s 청약 일정**\n\n오늘은 청약 일정이 없네요." % (date[1], date[0]))

if __name__ == "__main__":
  if len(sys.argv) > 1:
    main((sys.argv[1],''))
  else:
    now = datetime.datetime.now()
    dates = [(datetime.datetime.strftime(now, '%Y-%m-%d'),'오늘'), (datetime.datetime.strftime(now + datetime.timedelta(days=1), '%Y-%m-%d'), '내일')]
    [main(d) for d in dates]
