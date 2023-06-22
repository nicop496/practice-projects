import toga
import requests
from bs4 import BeautifulSoup
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class ConjugationsofEnglishVerbs(toga.App):
    def startup(self):
        self.verb_input = toga.TextInput(style=Pack( height=60, font_size=13))
        self.conjugate_btn = toga.Button('Conjugate', on_press=self.conjugate_verb, style=Pack(height=80, font_size=25,flex=4))
        self.verb_conj = toga.Label('\n', style=Pack(padding=5, text_align='center', font_size=16))


        main_box = toga.Box(style=Pack(direction=COLUMN, padding=5, alignment='center'))
        main_box.add(self.verb_input)
        main_box.add(self.conjugate_btn)
        main_box.add(self.verb_conj)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        
    def conjugate_verb(self, widget):
        verb = self.verb_input.value.lower()
        url = f'https://pasttenses.com/{verb}-past-tense'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        
        conjugations = [v.text for v in soup.find_all(class_='tg-6k2t')[1:4]]
        
        self.verb_conj.text = '\n\n\n'.join(conjugations)
        self.main_window.show()

def main():
    return ConjugationsofEnglishVerbs()

