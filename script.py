from typing import final
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
import os
import inquirer
from io import StringIO
import re

global parsedTable
global radioList
global radioLinks
global answer

URL = "http://piges.alexandremartinat.com"

#On parse la liste des radios accessible depuis le site
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
table = soup.find_all('table')[0] 
parsedTable = soup.find_all("tr", {'class':['col0', 'col1']})

#On trie les valeurs du tableau renvoyé par le site et nettoyé par BS
urls = []
for radioLinks in parsedTable:
    radioList = radioLinks.find_all("a")
    for channel in radioList:
        finalList = channel.text.strip()
    urls.append(finalList)  

#On demande la radio que l'utilisateur souhaite télécharger
chosen_radio = [
  inquirer.List('channelToDownload',
                message="Quelle chaîne souhaitez-vous télécharger ?",
                choices=urls
            ),
]
user_answer = inquirer.prompt(chosen_radio)
radio = user_answer.get('channelToDownload')
print("Downloading from", radio)

#On demande le jour que l'utilisateur souhaite télécharger
chosen_day = [
  inquirer.List('dayToDownload',
                message="Which day do you wish to download ?",
                choices=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
            ),
]
user_answer = inquirer.prompt(chosen_day)
day = user_answer.get('dayToDownload')
print("Downloading from", day)

#On demande l'heure que l'utilisateur souhaite télécharger
chosen_hour = [
  inquirer.List('hourToDownload',
                message="Quelle heure souhaitez-vous télécharger ?",
                choices=("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
            ),
]
user_answer = inquirer.prompt(chosen_hour)
hour = user_answer.get('hourToDownload')
print("Downloading from", hour,"hour")

#On définit le nom final du fichier selon la radio, le jour téléchargé et l'heure
final_name = radio+" - "+"Last "+day+" - "+hour+"h"
print("File will be named", final_name)

#Nous téléchargeons l'URL définie par les paramètres choisis
downloading_URL = URL+"/"+radio+"/"+day+"/"+hour+".mp3"
print("Download link is", downloading_URL)
download = requests.get(str(downloading_URL))
open(str(final_name)+str(".mp3"), 'wb').write(download.content)