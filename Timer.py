#Rhys Davies
#Application Timer
#11 Tech assignment Nov 2022

import os  #OS is required to access files properly and to stop programs
import configparser  #Configparser used for all of the INI read and write
import time
import winsound  #simple audio library
import ctypes  #Module for custom windows messages to show up
try:
    from playsound import playsound as ps
except:
    print("You do not have the correct modules installed")
    print("Please type this into command prompt")
    print("pip install playsound")
    input("Press ENTER to exit ")
    exit()

user = ""
timer = 30
warning = 5
untilWarning = 25
appOpen = ""
appClose = ""
appName = ""
presetDir = "presets"
found = False
again = ""
start = ""
startTime = ""

config = configparser.ConfigParser()
#os.system('TASKKILL /F /IM notepad.exe')
#os.startfile('presets\cubefield.ini')

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

createPreset = ""
preset = input("Do you have a previous preset? (y/n): ")

while preset.lower().strip() != "y" and preset.lower().strip() != "n":
    print("Not an option, please try again.")
    preset = input("Do you have a previous preset? (y/n): ")

while preset.lower().strip() == "y":
    presetName = input("What was the preset name: ")
    presetName += '.ini'
    for i in os.listdir(presetDir):
        f = os.path.join(presetDir, i)
        if os.path.isfile(f):  #this line is only so it does not print out folders, otherwise it is unnecesary
            f = os.path.split(f)
            if presetName == f[1]:
                config.read(f'presets\{presetName}')
                user = config['General'].get('user')
                #Timing
                timer = float(config['Timing'].get('timer'))
                warning = float(config['Timing'].get('warning'))
                #App
                appOpen = config['Application'].get('appopen')
                appClose = config['Application'].get('appclose')
                appName = config['Application'].get('name')
                
                print(f"{presetName} found.  Welcome back {user}")
                found = True
                break

    if found:
        break
    if not found:
        print(f"Could not find {presetName}")
        again = input("Would you like to try again? (y/n:) ")
        while again.lower().strip() != "y" and again.lower().strip() != "n":
            print("Not an option, please try again.")
            again = input("Would you like to try again? (y/n:) ")
        if again == "y":
            continue
        if again == "n":
            preset = "n"
            break
    

while preset.lower().strip() == "n":
    user = input('What is your name: ')
    appName = input(f"hi {user}, what app are you trying to close down: ")
    appOpen = input(f"What is the full path (including exe) of {appName}: ")
    ext = os.path.splitext(appOpen)[-1].lower()
    if ext == '.exe':
        appClose = appOpen
    else:
        appClose = input('Since this file is not an exe, what is the full path (including exe) of the application it opens with: ')
    while True:
        try:
            timer = float(input("How long do you want the timer to go for in minutes: "))
        except:
            print("Please input a number")
            continue
        break
    while True:
        try:
            warning = float(input("When do you want a warning to go off (minutes left): "))
        except:
            print("Please input a number")
            continue
        break

    createPreset = input('Would you like to save these settings as a preset to use later? (y/n): ')
    while createPreset.lower().strip() != "y" and createPreset.lower().strip() != "n":
        print("Not an option, please try again.")
        createPreset = input('Would you like to save these settings as a preset to use later? (y/n): ')

    if createPreset.lower().strip() == "y":
        presetName = input("What would you like to call the preset: ")
        config['General'] = {'user':user,'presetName':presetName}
        config['Timing'] = {'timer':timer,'warning':warning}
        config['Application'] = {'appOpen':appOpen,'appClose':appClose,'name':appName}
        with open(f'presets\{presetName}.ini', 'w') as configfile:
            config.write(configfile)
        break
    break


start = input("Do you have the program running already? (y/n): ")
while start.lower().strip() != "y" and start.lower().strip() != "n":
        print("Not an option, please try again.")
        start = input("Do you have the program running already? (y/n): ")

if start.lower().strip() == "y":
    startTime = input("Would you like to start the timer now? (y/n): ")
    while startTime.lower().strip() != "y" and startTime.lower().strip() != "n":
        print("Not an option, please try again.")
        startTime = input("Would you like to start the timer now? (y/n): ")

    if startTime.lower().strip() == "n":
        print("Ok Bye")
        time.sleep(2)
        exit()

if start.lower().strip() == "n":
    startTime = input("Would you like to start the timer and app now? (y/n): ")
    while startTime.lower().strip() != "y" and startTime.lower().strip() != "n":
        print("Not an option, please try again.")
        startTime = input("Would you like to start the timer and app now? (y/n): ")

    if startTime == "n":
        print("Ok Bye")
        time.sleep(2)
        exit()


    if startTime.lower().strip() == "y":
        os.startfile(f'{appOpen}')
        
untilWarning = timer - warning

time.sleep(untilWarning*60)
print(f'{warning} minutes left')
Mbox('WARNING', f'{warning} minutes remaining', 0)
winsound.PlaySound('alarm.wav', winsound.SND_ASYNC | winsound.SND_ALIAS)
time.sleep(warning*60)
appClose = os.path.split(appClose)
try:
    os.system(f'TASKKILL /F /IM {appClose[1]}')
except(Exception):
    print(str(Exception))
winsound.PlaySound('alarm.wav', winsound.SND_ASYNC | winsound.SND_ALIAS)
Mbox('Time Is Up', f'Time is Up!', 0)
print('Time is up!')
end = input("ENTER to quit")