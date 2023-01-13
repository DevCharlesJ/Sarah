#!/usr/bin/python3
AIAUDIOFILE = 'Sarah.mp3'

import os,time,warnings


answer_types = {
'intro': [
    'That would be ', "I believe that's ", "Pretty sure it's ", "I'm certain that it's ",
    'It has got to be ', "Surely it's "
],
'outro': [
    ' I believe.', ' if I remember correctly.', ' surely ', ''
]
}

greeting_types=['Hello','How may I be of service','Hi']
goodbye_types=['See you later', 'Goodbye for now', 'Adios', 'Farewell']


from gtts import gTTS
from mutagen.mp3 import MP3
# Need to integrate google Text-To-Speech or Mutgan.Mp3 for audible communication

def thenaudio(t):
    # Defaulted to english Version 1.0.0
    try:
        tts = gTTS(text=t, lang='en')
        tts.save(AIAUDIOFILE)
        os.system(AIAUDIOFILE)
        audio = MP3(AIAUDIOFILE)
        time.sleep(audio.info.length)
    except Exception as e:
        print(f"Error MSG: {e}")
        warnings.warn(f'GTTS or mutagen module error. Audible communication not available!\n')
        print('\nSpeech: ',t)


from random import randint
def random_selection(collection,super=False):
    if isinstance(collection, list):
        # IDEK it just does super? random selection and doesnt bug so all is well
        return random_selection(collection[randint(0,len(collection)-1)],True) if super else collection[randint(0,len(collection)-1)]
    elif isinstance(collection,dict):
        # same here
        if super:
            c = [v for i, v in collection.items()]
            return random_selection(c[randint(0,len(c)-1)],True)
        else:
            c = [[i, v] for i, v in collection.items()]
            return c[randint(0,len(c)-1)]
    else:
        return collection


def greet(name, out=False, rtn=False):
    name = ' '+ str(name)
    b, e = ('~| ', ' |~') if not out else ('','')

    output = random_selection(greeting_types)
    if out:
        thenaudio("".join([b, output, name, e]))
    else:
        if rtn:
            return "".join([b, output, name, e])
        else:
            print("".join([b, output, name, e]))



def goodbye(name, out=False, rtn=False):
    b, e = ('~| ', ' |~') if not out else ('','')

    output = random_selection(goodbye_types)
    if out:
        thenaudio("".join([b, output, name, e]))
    else:
        if rtn:
            return "".join([b, output, name, e])
        else:
            print("".join([b, output, name, e]))


class FORMAT:
    @staticmethod
    def to_special(text, out=False, rtn=False):
        text = str(text)
        b,e = ('~| ',' |~') if not out else ('','')

        if out:
            thenaudio("".join([b,text,e]))
        else:
            if rtn:
                return "".join([b,text,e])
            else:
                print("".join([b, text, e]))

    @staticmethod
    def to_error(text,out=False, rtn=False):
        text = str(text)
        b, e = ('!| Error ', " |!") if not out else ('','')

        if out:
            thenaudio("".join([b,text,e]))
        else:
            if rtn:
                return "".join([b,text,e])
            else:
                print("".join([b,text,e]))

    @staticmethod
    def to_answer(text,out=False, rtn=False):
        text = str(text)
        b, e = ('=| ',' |=') if not out else ('','')

        a_t = random_selection(answer_types)
        if a_t[0] == 'intro':
            output = random_selection(answer_types['intro'])
            text_char = list(text)
            text_char[0] = text_char[0].lower()
            text = ''.join(text_char)
            if out:
                thenaudio("".join([b, output, text, e]))
            else:
                if rtn:
                    return "".join([b, output, text, e])
                else:
                    print("".join([b, output, text, e]))
        else:
            if a_t[0] == 'outro':
                output = random_selection(answer_types['outro'])
                if out:
                    thenaudio("".join([b, text, output, e]))
                else:
                    if rtn:
                        return "".join([b, text, output, e])
                    else:
                        print("".join([b, text, output, e]))

    @staticmethod
    def normal(text,out=False, rtn=False):
        text = str(text)
        b,e = ('| ',' |') if not out else ('','')

        if out:
            thenaudio("".join([b,text,e]))
        else:
            if rtn:
                return "".join([b,text,e])
            else:
                print("".join([b,text,e]))

    @staticmethod
    def to_group(collection,out=False, rtn=False,alone=False):

        collection = [str(el) for el in collection]

        b, e = ('| ', ' |') if not out else ('','')

        limit = 10

        text = ', '.join(collection[:limit if limit < len(collection) else None])

        if len(collection) > limit:
            text += f' and {len(collection) - limit} more items'

        if out and not alone:
            thenaudio("".join([b,text,e]))
        elif not alone:
            if rtn:
                return "".join([b,text,e])
            else:
                print("".join([b,text,e]))
        elif out and alone:
            thenaudio(text)
        elif alone:
            if rtn:
                return text
            else:
                print(text)


if __name__ == '__main__':
    formatter = FORMAT()
    formatter.normal("Hello!", out=True)