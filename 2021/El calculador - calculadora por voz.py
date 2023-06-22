from speech_recognition import Recognizer, Microphone, UnknownValueError
from gtts import gTTS
from playsound import playsound
from shutil import rmtree as delete_folder
import os

AUDIO_FOLDER = 'palabras_del_calculador'
if not os.path.exists(os.getcwd() + '\\' + AUDIO_FOLDER):
    os.mkdir(AUDIO_FOLDER)
else:
    delete_folder(AUDIO_FOLDER)
    os.mkdir(AUDIO_FOLDER)

def text_to_voice(string):
    text_to_speech = gTTS(string, lang='es')
    file = f'{AUDIO_FOLDER}/audio.mp3'
    text_to_speech.save(file)
    playsound(file)
    os.remove(file)

try:
    r = Recognizer()
    
    with Microphone() as source:
        r.adjust_for_ambient_noise(source)
        text_to_voice('Dime tu cálculo.')
        audio = r.listen(source)
        

    text_to_voice('Ok. Estoy procesando, recuerda que soy una computadora.')
    speech = r.recognize_google(audio, language='es-ES')
    text_to_voice('Te entendí ' + speech.replace('*', 'por'))
    
    for old, new in {'más':                '+',
                     'menos':              '-',
                     'por':                '*',
                     'x':                  '*',
                     'dividido':           '/',
                     'abrir paréntesis':   '(',
                     'cerrar paréntesis':  ')',
                     'al cuadrado':        '**2',
                     'al cubo':            '**3',
                     'elevado':            '**',
                     ' ':                  '',
                     'uno':                '1',
                     'dos':                '2',
                 }.items():
        speech = speech.replace(old, new)
    
    text_to_voice('Y medio como resultado ' +  str(eval(speech)))
    

except UnknownValueError:
    text_to_voice('Lo siento, no te entendí.')

except (SyntaxError, NameError):
    text_to_voice('Lo que dijiste no lo entiendo como un cálculo.')

except ZeroDivisionError:
    text_to_voice('¡¡¡No puedes dividir por cero!!!')

finally:
    delete_folder(AUDIO_FOLDER)
    from time import sleep
    sleep(5)
