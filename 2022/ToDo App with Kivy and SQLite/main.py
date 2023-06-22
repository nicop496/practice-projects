import sqlite3 as sql

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

Builder.load_string('''
#:import utils kivy.utils

<NotesScreen>:
    orientation: 'vertical'
    canvas:
        Color:
            rgb: utils.get_color_from_hex('#1b1b1f')
        Rectangle:
            size: self.size
            pos: self.pos
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            id: notes_container
            size_hint_y: None
            height: self.minimum_height
    Button:
        id: create_btn
        text: 'Create new note'
        size_hint: 1, .175
        on_release: root.create_note_btn()

<Note>:
    size_hint_y: None
    height: '45dp'
    CheckBox:
        id: check_box
        size_hint_x: None
        width: '30dp'
        disabled: txt_input.focused
        on_release: root.check_box_btn(self.active)
    TextInput:
        id: txt_input
        multiline: False
        font_size: '25dp'
        on_focus: if self.focused == False: root.update_note_content()
    Button:
        text: 'Delete'
        size_hint_x: None
        width: '60dp'
        on_release: root.delete_note_btn()
        background_color: utils.get_color_from_hex('#b2bdd6')
'''
)


def db_query(command):
    connection = sql.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute(command)
    records = cursor.fetchall()
    connection.commit()
    connection.close()
    return records


class NotesScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        records = db_query("SELECT id, content, checked FROM notes ORDER BY id ASC;")
        for id, content, checked in records:
            note = Note(id)
            note.ids.check_box.active = bool(checked)
            note.ids.txt_input.text = content
            note.ids.txt_input.disabled = bool(checked)
            self.ids.notes_container.add_widget(note)

    def create_note_btn(self):
        db_query(f"INSERT INTO notes (content, checked) VALUES ('', 0);")
        new_note = Note(db_query("SELECT max(id) FROM notes")[0][0])
        self.ids.notes_container.add_widget(new_note)
        new_note.ids.txt_input.focused = True
        return new_note


class Note(BoxLayout):
    def __init__(self, db_id, **kwargs):
        super().__init__(**kwargs)
        self.db_id = db_id

    def delete_note_btn(self):
        self.parent.remove_widget(self)
        db_query(f"DELETE FROM notes WHERE id = {self.db_id};")

    def update_note_content(self):
        content = self.ids.txt_input.text
        db_query(f"UPDATE notes SET content = '{content}' WHERE id = {self.db_id};")

    def check_box_btn(self, check_box_status):
        self.ids.txt_input.disabled = check_box_status
        db_query(f"UPDATE notes SET checked = {int(check_box_status)} WHERE id = {self.db_id};")


class MainApp(App):
    title = 'To-Do App'
    def build(self):
        return NotesScreen()


if __name__ == '__main__':   
    db_query(
        '''
        CREATE TABLE IF NOT EXISTS notes (
            "id"	INTEGER NOT NULL,
            "content"	TEXT NOT NULL,
            "checked"	INTEGER NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        )
        '''
    )
    MainApp().run()
