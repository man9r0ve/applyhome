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

def __getLogger():
  with open("./logging.json", "rt") as file:
    config = json.load(file)
  
  logging.config.dictConfig(config)
  
  return logging.getLogger()

def getTypeName(cal_datas, index):
    class_list = ['lb_special' ,'lb_one', 'lb_two', 'lb_office', 'lb_simin','lb_resid','lb_adv_special', 'lb_adv_one','lb_adv_two']
    desc_list  = ['APT 특별공급' ,'APT 1순위', 'APT 2순위', '오피스텔/도시형생활주택/민간임대', '공공지원민간임대','무순위/취소후재공급','민간사전청약 APT 특별공급', '민간사전청약 APT 1순위','민간사전청약 APT 2순위']
    
    for iclss, clss in enumerate(class_list):
        if cal_datas[index].evaluate('el => el.classList.contains("%s")' % clss):
            return desc_list[iclss]
        else:
            return ""

def run(playwright: Playwright) -> None:

    #logger 생성
    global logger
    logger = __getLogger()

    # chrome 브라우저를 실행
    arguments = [
        "--lang=ko_KR",
        "--disable-blink-features=AutomationControlled",
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        "--disable-blink-features=AutomationControlled"
    ]

    browser = playwright.chromium.launch(headless=True, args=arguments)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    page.goto("https://www.applyhome.co.kr/ai/aib/selectSubscrptCalenderView.do")
    page.wait_for_load_state(state='load')
    time.sleep(3)

    cal_table = page.query_selector_all("xpath=/html/body/div[1]/div[6]/div[2]/div[2]/table/tbody/tr/td/a")

    cal_datas = page.query_selector_all("xpath=/html/body/div[1]/div[6]/div[2]/div[2]/table/tbody/tr/td/a/span")

    cal_date = []
    for elmt in cal_table:
        _data = elmt.inner_text().replace("\n","|").split("|")
        cal_date.append(_data[0])

    # 중복날짜 제거
    cal_date = list(dict.fromkeys(cal_date))

    # 최종 데이터를 담을 json
    apply_json = {}
    for date in cal_date:
        # 같은 날의 청약정보를 담을 리스트
        home_list = []
        for index, elmt in enumerate(cal_table):
            _data = elmt.inner_text().replace("\n","|").split("|")

            if date == _data[0]:
                # 청약정보를 담을 json
                home = {}
                home['name'] = _data[1]
                home['type'] = getTypeName(cal_datas, index)
                home['link'] = 'https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancDetail.do?houseManageNo=%s&pblancNo=%s&houseSecd=%s' % (cal_datas[index].get_attribute("data-hmno"), cal_datas[index].get_attribute("data-pbno"), cal_datas[index].get_attribute("data-se"))
                #print(home)
                home_list.append(home)

        #print(date, ">> ", home_list)
        apply_json[date] = home_list

    """
    print("------------")
    print(apply_json)
    """
    with open('applyhome.json', 'w', encoding="utf-8") as make_file:
        json.dump(apply_json, make_file, ensure_ascii=False, indent="\t")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)