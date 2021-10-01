import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import datetime
import webbrowser

PATH = "C:\Program Files (x86)\chromedriver.exe"


def close(userInput):
    if userInput == "q":
        return True
    else:
        return False


options = Options()
options.add_argument('--headless')
options.add_argument('--profile-directory=Default')
driver = webdriver.Chrome(options=options, executable_path=PATH)

driver.get("https://www.yr.no/nb/v%C3%A6rvarsel/daglig-tabell/1-211102/Norge/Tr%C3%B8ndelag/Trondheim/Trondheim")

print(driver.title)

weekdays = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
weekDayInt = datetime.datetime.today().weekday()

time.sleep(1)

degree_num = driver.find_element_by_xpath(
    '/html/body/div[1]/div/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/span')
weather_num = driver.find_element_by_xpath(
    '/html/body/div[1]/div/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[2]/div[2]/div/span/span[2]')
print("Været i trondheim er: " + degree_num.text)
print("Nedbør: " + weather_num.text + "mm")

# Input fra brukeren, som kan velge hvilken dag han vil ha værvarselet for
wantMoreDays = 1
x = 0
userInput = ""

while wantMoreDays == 1:

    f = open("weatherTrondheim.txt", "w")
    f.write("I trondheim er det for øyeblikket " + degree_num.text + " grader!\n")

    if float(weather_num.text) == 0:
        f.write("Det er ingen nedbør\n")
    else:
        f.write("Det er foreløpig " + weather_num.text + " mm nedbør\n")

    f.close()

    format1 = ""

    while x == 0:
        userDay = input("Hvilken dag vil du ha værvarselet for? 0=idag, 1=imorgen ..\n")

        if close(userDay):
            print("Ha en fin dag, Håkon! Bruk tiden godt :)")
            exit()

        try:
            if int(userDay) < 0 or int(userDay) > 6:
                print("Input må et tall fra 0-6")
            else:
                x = 1
                userInput = userDay
        except TypeError:
            print("Skriv inn gyldig input")
        except:
            print("Skriv inn gyldig input")

        newLine = input("Vis i fil eller konsoll? f/k: \n")

        if close(newLine):
            print("Ha en fin dag, Håkon! Bruk tiden godt :)")
            exit()

        if newLine == "f":
            x = 1
        elif newLine == "k":
            format1 = "k"

    today_grid = driver.find_element_by_id("dailyWeatherListItem" + str(int(userInput)))
    today_grid.click()

    today_elements = driver.find_elements_by_class_name("fluid-table__row")

    result = 0

    print("\nViser værmelding for " + weekdays[weekDayInt + int(userInput)] + ": \n")

    if format1:
        print("Værmelding for " + weekdays[weekDayInt + int(userInput)] + ":\n")
        for q in today_elements:
            textList = q.text.splitlines()

            ### Dette som feiler
            # if textList[3] > 25:
            #    print("Kl " + textList[0] + " er det meldt " + textList[3] + " grader!!!!!! ")
            # else:
            print("Kl " + textList[0] + " er det meldt " + textList[3] + " grader! ")
    else:

        f = open("weatherTrondheim.txt", "w")

        f.write("Værmelding for " + weekdays[weekDayInt + int(userInput)] + ":\n")

        if int(userInput) == 0:
            # f.write("I trondheim er det for øyeblikket " + degree_num.text + " grader!\n")

            if float(weather_num.text) == 0:
                f.write("Det er ingen nedbør\n")
            else:
                f.write("Det er foreløpig " + weather_num.text + " mm nedbør\n")

        for e in today_elements:
            textList = e.text.splitlines()
            f.write("kl " + textList[0] + " er det meldt " + textList[3] + " grader! \n")

        f.close()

        webbrowser.open("weatherTrondheim.txt")

    anotherDay = input("Vil du ha værvarselet for en annen dag? j/n \n")

    if close(anotherDay):
        print("Ha en fin dag, Håkon! Bruk tiden godt :)")
        exit()

    ok = 0

    while ok == 0:
        if anotherDay == "j":
            wantMoreDays = 1
            driver.back()
            x = 0
            ok = 1
        elif anotherDay == "n":
            wantMoreDays = 0
            ok = 1
        else:
            print("Skriv inn j (ja) eller n (nei)\n")
            anotherDay = input("Vil du ha værvarselet for en annen dag? j/n \n")
            if close(anotherDay):
                print("Ha en fin dag, Håkon! Bruk tiden godt :)")
                exit()

driver.close()

print("\nHa en fin dag, Håkon! Bruk tiden godt :)")
