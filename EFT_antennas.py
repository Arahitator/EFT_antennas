import requests
import re
from bs4 import BeautifulSoup
import json
import getpass

url = "https://bp.eft-cors.ru/login"
url2 = "https://bp.eft-cors.ru/basestations/"
mail = input("Введите почту (аккаунта EFT-cors): ")
password = getpass.getpass("Введите пароль: ")
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/"
              "webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "93",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "bp.eft-cors.ru",
    "Origin": "https://bp.eft-cors.ru",
    "Referer": "https://bp.eft-cors.ru/login",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                  "85.0.4183.102 Safari/537.36"
}

with requests.Session() as session:
    a = session.get(url)
    soup = BeautifulSoup(a.text, "html.parser")
    token = soup.input["value"]
    session.post(url, {
        "_token": token,
        "email": mail,
        "password": password
    })
    print("Соединение с сайтом установлено.")
    antennas = {}
    for i in range(1000):
        print(str(i + 1) + " ")
        content = session.get(url2 + str(i + 1))
        if content:
            soup = BeautifulSoup(content.text, "html.parser")
            first = soup.find("div", string=re.compile("Код"))
            ID = first.find_next_sibling("div").get_text().replace("\n", "").split()[0]
            second = soup.find("div", string=re.compile("Тип антенны:"))
            ant_type = second.find_next_sibling("div").get_text().replace("\n", "")
            if "EFT A1" in ant_type:
                ant_type = "EFT_A1"
            elif "EFT A2" in ant_type:
                ant_type = "EFT_A2"
            elif "Zephyr Geodetic" in ant_type or "Zephyr Geodethic" in ant_type:
                ant_type = "TRM55971.00"
            elif "Trimble Zephyr2" in ant_type:
                ant_type = "TRM55970.00"
            elif "AS10" in ant_type:
                ant_type = "LEIAS10"
            else:
                ant_type = "Unknown - " + ant_type
            print(f"Добавлена станция {ID} - {ant_type}")
            antennas[ID] = ant_type
    with open("eft_antennas.json", "w") as file:
        json.dump(antennas, file)
