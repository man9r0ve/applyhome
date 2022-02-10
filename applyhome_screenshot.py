from playwright.sync_api import Playwright, sync_playwright
import time
import random

import os
from pathlib import Path

from datetime import datetime

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
      list = applyhome[date]

      for el in list:
        parsed_url = "https://m.map.naver.com/search2/search.naver?query=%s&sm=hty&style=v5#/search" % quote(el['addr'])
        #sendTgBot("**%s 청약 일정**\n\n[%s - %s]\n[%s](%s)\n\n[네이버 지도로 보기](%s)\n[구글 지도로 보기](https://www.google.com/maps/search/%s)" % (date, el['type'], el['short_addr'], el['name'], el['link'], parsed_url, quote(el['addr'])))
        sendTgBot("**%s 청약 일정**\n\n[%s - %s]\n[%s](%s)\n\n[네이버 지도로 보기](%s)" % (date, el['type'], el['short_addr'], el['name'], el['link'], parsed_url))
    except Exception as e:
      sendTgBot("**%s 청약 일정**\n\n오늘은 청약 일정이 없네요." % date)

if __name__ == "__main__":
  
  if len(sys.argv) > 1 :
    main(sys.argv[1])
  else:
    main(datetime.strftime(datetime.now(), '%Y-%m-%d'))
