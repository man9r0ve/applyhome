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

CHAT_TOKEN = "5057248274:AAG5ZLh2968zEE9282_-FkGuaYas5USIfww"
CHAT_ID = "543572618"

def __getLogger():
  with open("./logging.json", "rt") as file:
    config = json.load(file)
  
  logging.config.dictConfig(config)
  
  return logging.getLogger()

#텔레그램봇으로 전송
def sendTgBot(text):
  bot = telegram.Bot(token=CHAT_TOKEN)
  bot.sendMessage(chat_id=CHAT_ID, text=text, parse_mode="markdown")

def getTypeName(cal_datas, index):
    class_list = ['lb_special' ,'lb_one', 'lb_two', 'lb_office', 'lb_simin','lb_resid','lb_adv_special', 'lb_adv_one','lb_adv_two']
    desc_list  = ['APT 특별공급' ,'APT 1순위', 'APT 2순위', '오피스텔/도시형생활주택/민간임대', '공공지원민간임대','무순위/취소후재공급','민간사전청약 APT 특별공급', '민간사전청약 APT 1순위','민간사전청약 APT 2순위']
    
    for iclss, clss in enumerate(class_list):
        if cal_datas[index].evaluate('el => el.classList.contains("%s")' % clss):
            return desc_list[iclss]

def run(playwright: Playwright) -> None:
    #logger 생성
    global logger
    logger = __getLogger()

    sendTgBot("[2021-02-10 내포신도시 모아미래도 메가시티 2차(APT 특별공급)](https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancDetail.do?houseManageNo=2022000041&pblancNo=2022000041&houseSecd=01)")

    """with open("./applyhome.json", "r", encoding="utf-8") as jsonData:
        applyhome = json.load(jsonData)

    print("##########")
    print(applyhome)

    # chrome 브라우저를 실행
    arguments = [
        "--lang=ko_KR",
        "--disable-blink-features=AutomationControlled",
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        "--disable-blink-features=AutomationControlled",
        "--width=800px"
    ]

    browser = playwright.chromium.launch(headless=True, args=arguments)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancDetail.do?houseManageNo=2021000844&pblancNo=2021000844&houseSecd=01")
    time.sleep(3)
    #page.wait_for_load_state(state='load')
    page.screenshot(path = "screenshot.png", full_page=True)

    context.close()
    browser.close()"""

with sync_playwright() as playwright:
    run(playwright)