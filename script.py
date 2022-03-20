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
parsedTable = soup.find_all("tr", class_="col1")

#On trie les valeurs du tableau renvoyé par le site et nettoyé par BS
urls = []
for radioLinks in parsedTable:
    radioList = radioLinks.find_all("a")
    for channel in radioList:
        finalList = channel.text.strip()
    urls.append(finalList)  

#On demande la radio que l'utilisateur souhaite télécharger
whichChannelToDownload = [
  inquirer.List('channelToDownload',
                message="Quelle chaîne souhaitez-vous télécharger ?",
                choices=urls
            ),
]
userAnswerRadio = inquirer.prompt(whichChannelToDownload)
userAnswerRadioFirstParsing=str(userAnswerRadio).replace("{'channelToDownload': '", '')
userAnswerRadioFinalParsing=str(userAnswerRadioFirstParsing).replace("'}", '')
radio = userAnswerRadioFinalParsing
print("Nous allons télécharger", radio)

#On demande le jour que l'utilisateur souhaite télécharger
whichDayToDownload = [
  inquirer.List('dayToDownload',
                message="Quel jour souhaitez-vous télécharger ?",
                choices=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
            ),
]
userAnswerDay = inquirer.prompt(whichDayToDownload)
userAnswerDayFirstParsing=str(userAnswerDay).replace("{'dayToDownload': '", '')
userAnswerDayFinalParsing=str(userAnswerDayFirstParsing).replace("'}", '')
day = userAnswerDayFinalParsing
print("Nous allons télécharger l'émission de", day)


#On demande l'heure que l'utilisateur souhaite télécharger
whichHourToDownload = [
  inquirer.List('hourToDownload',
                message="Quelle heure souhaitez-vous télécharger ?",
                choices=("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
            ),
]
userAnswerHour = inquirer.prompt(whichHourToDownload)
userAnswerHourFirstParsing=str(userAnswerHour).replace("{'hourToDownload': '", '')
userAnswerHourFinalParsing=str(userAnswerHourFirstParsing).replace("'}", '')
hour = userAnswerHourFinalParsing
print("Nous allons télécharger l'émission de", hour,"h")

#On définit le nom final du fichier selon la radio, le jour téléchargé et l'heure
finalName = radio+" - "+"Last "+day+" - "+hour+"h"
print(finalName)

#Nous téléchargeons l'URL définie par les paramètres choisis
beginURL = "http://pige.alexandremartinat.com/"
finalURL = beginURL+radio+"/"+day+"/"+hour+".mp3"
print(finalURL)
download = requests.get(str(finalURL))
open(str(finalName)+str(".mp3"), 'wb').write(download.content)


######################################################################
# today = date.today()
# print(today)
# todayName = today.strftime("%A")

# nbArgsCLI = len(sys.argv)-1
# print("Vous avez passé", nbArgsCLI, "arguments.")

# #Si aucune émission demandée dans le CLI au format "Monday", on télécharge l'émission du jour
# global dayToDownload 
# if int(nbArgsCLI) == 0:
#     dayToDownload = todayName
#     print("Aucun jour spécifié, nous téléchargeons aujourd'hui")
#     finalName = today

# else:
#     dayToDownload = str(sys.argv[1])
#     print("Nous allons télécharger", dayToDownload)
#     finalName = "Last " + dayToDownload
    

# #Quelle heure on souhaite télécharger ?
# hourToDownload = 21
# beginURL = "http://pige.alexandremartinat.com/Frequence3/"
# endURL = str(hour)+".mp3"
# finalURL = beginURL+dayToDownload+"/"+endURL
# #URL de test: finalURL = "http://localhost/test.png"
# download = requests.get(str(finalURL))
# open(str(finalName)+str(".mp3"), 'wb').write(download.content)