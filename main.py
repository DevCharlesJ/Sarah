#!/usr/bin/python3



# Sniff for required modules
from _moduleHound import sniff
sniff()


DATABASE = 'DATABASE.JSON'
try:
    with open(DATABASE, 'r') as r_db:
        if r_db.read() == "":
            with open(DATABASE, 'w') as w_db:
                w_db.write('{}')

except FileNotFoundError:
    with open(DATABASE,'w') as db:  # To initialize a database if none exists
        db.write('{}')


from internal import COMMUNICATION, DBManager, Processor
import speech_recognition as sr
from os import system



__on__ = True
input_type, botaudio = 'typed', True

def startup():
    print("[LOGIN]")
    COMMUNICATION.FORMAT.normal('Please enter your Username', out=botaudio)
    user_name = input('<- ').strip()
    user = DBManager.DATA.get(user_name)
    if user: # TYPE: DICT
        pwd = None # TYPE: STR
        while pwd is None or pwd != user['password']:
            if pwd: # pwd not None means user made an attempt
                COMMUNICATION.FORMAT.to_error('Error, Incorrect Password! Please try again', out=botaudio)

            COMMUNICATION.FORMAT.normal('Please enter your password', out=botaudio)
            pwd = input('<- ')

        return user_name


    COMMUNICATION.FORMAT.normal(f'Hi {user_name}, it is nice to meet you! As a new user, I am required to have a password for your account.', out=botaudio)
    
    # NO PASSWORD CHECKER or ENCRYPTION
    new_pwd, confirm_pwd = None, None

    while new_pwd is None or new_pwd != confirm_pwd:
        if new_pwd: # new_pwd not None means user made an attempt
            COMMUNICATION.FORMAT.to_error('ERROR. Your entries did not match! Please try again', out=botaudio)

        COMMUNICATION.FORMAT.normal('Please type a safe password to be linked with your account', out=botaudio)
        new_pwd = input('<-')

        COMMUNICATION.FORMAT.normal('Please re-enter your password for confirmation', out=botaudio)
        confirm_pwd = input('<- ')

    DBManager.DATA.create_directory(p=None,dir_name=user_name)
    DBManager.DATA.add_data(p=f'{user_name}', new_data={"password": new_pwd})
    DBManager.DATA.create_directory(p=f'{user_name}',dir_name='-custom-library')  # create custom library directory

    for preset_data in 'morning,afternoon,night,evening,meridiem,time,date,today,day,month,year'.split(','):
        DBManager.DATA.add_data(p=f'{user_name}', new_data={preset_data:''})

    COMMUNICATION.FORMAT.normal('Thank you, you\'re all set and ready to go!', out=botaudio)
    return user_name


USER = startup()  # USER is just user's user_name

system("cls")
greet = COMMUNICATION.random_selection(COMMUNICATION.greeting_types, super=True)
COMMUNICATION.FORMAT.to_special(f'{greet}, {USER}', botaudio)


r = sr.Recognizer()
Microphone = None
try:
    Microphone = sr.Microphone()
except OSError:
    pass

check = r and Microphone

while __on__:
    print()   # So each run output is seperated
    #For typing
    if input_type == 'typed':
        entry = input('-> ')

        system("cls")
        print(f"-> {entry}")
        run = Processor.process(entry,USER, botaudio)
        if run == 'shutdown':
            __on__ = False
        elif run == 'switch input':
            if check:
                input_type = 'audible'
                COMMUNICATION.FORMAT.normal(f"Input switched to microphone", out=botaudio)
        elif run == 'switch output':
            botaudio = not botaudio
            COMMUNICATION.FORMAT.normal(f'Bot audio switch to {botaudio}', out=False)

    #For microphone
    elif input_type == 'audible':
        try:
            print("I'm Listening ~(=...")
            with Microphone as source:
                r.adjust_for_ambient_noise(source,duration=1)
                audio = r.listen(source)
                text = r.recognize_google(audio)

                system("cls")
                COMMUNICATION.FORMAT.normal(f'{text}?', out=False)
                run = Processor.process(text,USER, botaudio)
                if run == 'shutdown':
                    __on__ = False
                elif run == 'switch input':
                    input_type = 'typed'
                    COMMUNICATION.FORMAT.normal(f"Input switched to typed", out=botaudio)
                elif run == 'switch output':
                    botaudio = not botaudio
                    COMMUNICATION.FORMAT.normal(f'Bot audio switch to {botaudio}', out=False)

        except sr.UnknownValueError as e:
            COMMUNICATION.FORMAT.normal(f"Sorry, I don't understand", out=botaudio)
        except sr.RequestError as e:
            pass


goodbye = COMMUNICATION.random_selection(COMMUNICATION.goodbye_types, super=True)
COMMUNICATION.FORMAT.to_special(f'{goodbye}, {USER}!', out=botaudio)