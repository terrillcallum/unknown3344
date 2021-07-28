import base64
import os

from discord_webhook import DiscordWebhook
import requests
from PIL import Image
from pytesseract import pytesseract
import pyautogui
from PIL import ImageGrab
import time
from fuzzywuzzy import fuzz
from win32api import GetSystemMetrics

directory = os.getcwd()
pytesseract.tesseract_cmd = rf'''{directory}\tesseract\tesseract.exe'''

def send_discord_alert(message, image):
    url = 'https://discord.com/api/webhooks/870000059033456640/flkPLmF019VxTdBtMocIgQfQ8EHRsOjBRi1bG4Vufqz_gWUfcuYzdoM2j9zGxSnD-dWG'
    discordContents = {'content': message}

    x = requests.post(url, data=discordContents)

    print(x.text)

def translate(message):

    message_array = message.split(" ")
    corrected_message = ""
    counter = 0
    for word in message_array:
        word = word.lower()
        #print(word)
        if fuzz.ratio(word,"auto-decay") > 60 : #in data:
            corrected_message += f"auto-decay "
            counter -= 1
        elif fuzz.ratio(word,"destroyed") > 60 : #in data:
            corrected_message += f"destroyed "
            counter += 1
        elif fuzz.ratio(word, "killed") > 60 : #in data:
            corrected_message += f"killed "
            counter += 1
        elif fuzz.ratio(word, "enemy") > 60 : #in data:
            corrected_message += f"killed "
            counter += 1
        elif fuzz.ratio(word,"destroyed") > 60 : #in data:
            corrected_message += f"destroyed "
            counter += 1
        else:
            if word == "destroyed" or word == "destroyed!":
                counter += 1
            corrected_message += f"{word} "


    return corrected_message, counter


print("Width =", GetSystemMetrics(0))
print("Height =", GetSystemMetrics(1))


while True:
    screenshot = pyautogui.screenshot()
    image = ImageGrab.grab(bbox=((GetSystemMetrics(0)*0.6875), (GetSystemMetrics(1)*0.16666), (GetSystemMetrics(0)*0.9375), (GetSystemMetrics(1)*0.4444)))
    image.save("sample1.jpg")
    im = Image.open("sample1.jpg")

    text = pytesseract.image_to_string(im, lang = 'eng', config="--psm 6")
    correct_message, counter = translate(text)
    print(counter, correct_message)
    if counter > 2:
        print("detected")
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/870000059033456640/flkPLmF019VxTdBtMocIgQfQ8EHRsOjBRi1bG4Vufqz_gWUfcuYzdoM2j9zGxSnD-dWG', username="ark alert bot")
        # send two images
        with open("sample1.jpg", "rb") as f:
            webhook.add_file(file=f.read(), filename='example.jpg')
        response = webhook.execute()
    time.sleep(10)
