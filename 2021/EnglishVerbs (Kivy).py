import requests
from bs4 import BeautifulSoup

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class Aplicacion(BoxLayout):
    def __init__(self):
        super(Aplicacion, self).__init__()
        with self.canvas:
            Color(.32,.22,.86,.2)
            Rectangle(pos=(0,0), size=(2000,2000))

        self.orientation = 'vertical'
        self.padding = 9
        self.spacing = 9
        
        self.verbo_txtinput = TextInput(text='',
                                        multiline=False,
                                        size_hint=(1, .1),
                                        font_size=35
                                        )

        conjugar_btn = Button(text='Conjugar', 
                              size_hint=(1, .2), 
                              on_press=self.conjugar_verbo,
                              font_size=24)

        self.conjugacion_label = Label(size_hint=(1, .7), 
                                       font_size=28, 
                                       halign='center', 
                                       valign='bottom')

        self.add_widget(self.verbo_txtinput)
        self.add_widget(conjugar_btn)
        self.add_widget(self.conjugacion_label)

    def conjugar_verbo(self, *args):
        verbo = self.verbo_txtinput.text.lower()
        print(verbo)
        url = f'https://pasttenses.com/{verbo}-past-tense'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        
        c = [v.text for v in soup.find_all(class_='tg-6k2t')[1:4]]
        
        self.conjugacion_label.text= '\n\n\n'.join(c) if len(c) > 0 else 'no sé :('
    

class MyApp(App):
    title = 'English verbs'
    def build(self):
        return Aplicacion()


MyApp().run()