import kivy
import time

from kivy.app import App
from kivy.properties import *
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class Aplicacion(BoxLayout):
    colores = ([0,0,0],[0,0,1],[0,.8,0],[1,0,0],[.8,.8,.0],[.2,.2,.2],)
    color_actual = 0
    color = ListProperty(colores[color_actual])

    clicks = NumericProperty()
    segundos = NumericProperty()
    empezar = BooleanProperty(False)
    
    def __init__(self):
        super(Aplicacion, self).__init__()
        # Boton de clicks
        self.click_btn = Button(
            size_hint=(1,.5),
            text='click',font_size=15,
            on_press=self.click,
            )
        # BoxLayout de botones "cambiar color" y "repetir"
        self.botones = BoxLayout(size_hint=(1,.1))
        self.cambiar_color_btn = Button(
            text='cambiar_color',
            on_press=self.cambiar_color,
            )
        self.repetir_btn = Button(
            text='repetir',
            disabled=True,
            on_press=self.repetir,
            )
        self.botones.add_widget(self.cambiar_color_btn,)
        self.botones.add_widget(self.repetir_btn)
        #--------#
        self.add_widget(self.click_btn)
        self.add_widget(self.botones)

        Clock.schedule_interval(self.update, 0.01)

    def update(self, *args):
        if self.empezar:
            self.segundos += 0.01
            self.segundos = round(self.segundos, 3)
            self.repetir_btn.disabled = True
        
        if self.segundos >= 5:
            self.empezar = False
            self.click_btn.disabled = True
            self.click_btn.text = f'{round(self.clicks / 5, 5)} clicks por segundo'
            self.repetir_btn.disabled = False
        else:
            self.click_btn.disabled = False
            self.click_btn.text = 'click'
            self.repetir_btn.disabled = True

    def click(self, *args):
        self.clicks += 1
        self.empezar = True
    
    def repetir(self, *args):
        self.segundos = 0
        self.clicks = 0

    def cambiar_color(self, *args):
        if self.color_actual < len(self.colores)-1:
            self.color_actual += 1
        else:
            self.color_actual = 0

        self.color = self.colores[self.color_actual]


class MainApp(App):
    title='Clicks por segundo'
    def build(self):
        return Aplicacion()

if __name__ == '__main__':
    MainApp().run()