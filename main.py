from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, \
    QVBoxLayout, QInputDialog
import json


notes = {
    "Гарного дня!":{
        "текст" : "",
        "теги" : ["Тег1","Тег2"]
    },
    "Домашка" : {
        "текст" : "Доробити домашку на понеділок",
        "теги" : ["Фізіка","Хімія","Математика"]

    }
}

app = QApplication([])

window = QWidget()
window.setWindowTitle("Розумні замітки")
window.resize(900,600)

list_notes = QListWidget()
list_notes_label = QLabel("Список заміток")

button_note_create = QPushButton("Створити замітку")
button_note_del = QPushButton("Видалити замітку")
button_note_save = QPushButton("Зберегти замітку")

field_tag = QLineEdit("")
field_tag.setPlaceholderText("Введіть тег...")
field_text = QTextEdit()
list_tags = QListWidget()
list_tags_label = QLabel("Список тегів")
button_tag_add = QPushButton("Додати до замітки")
button_tag_del = QPushButton("Відкріпити від замітки")
button_tag_search = QPushButton("Шукати замітки по тегу")

layout_notes = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(field_text)

col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)
row1 = QHBoxLayout()
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)
row2 = QHBoxLayout()
row2.addWidget(button_note_save)
col2.addLayout(row1)
col2.addLayout(row2)

col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)
row3 = QHBoxLayout()
row3.addWidget(button_tag_add)
row3.addWidget(button_tag_del)
row4 = QHBoxLayout()
row4.addWidget(button_note_save)

col2.addLayout(row3)
col2.addLayout(row4)

layout_notes.addLayout(col1, stretch=2)
layout_notes.addLayout(col2, stretch=1)
window.setLayout(layout_notes)

def show_notes():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def create_note():
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Нава замітки")
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key][key]["текст"] = field_text.toPlainText()
        with open("note_data.json","w") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print("Замітка для додавання не обрана")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags()
        field_text()
        list_notes.addItems(notes)
        with open("note_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print("Замітка для додавання не обрана")
        
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("note_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print("Замітка для додавання не обрана")


def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json","w") as file:
            json.dump(notes, file, sort_key=True)
    else:
        print("Тег для видалення не обраний!")

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Шукати замітки по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Скинути пошук")
        field_tag.clear()
        list_notes.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Скинути пошук":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        button_tag_search.setText("Шукати Замітки по тегу")




with open("note_data.json","w") as file:
    json.dump(notes,file)

with open("note_data.json","r") as file:
    notes = json.load(file)
list_notes.addItems(notes)

list_notes.itemClicked.connect(show_notes)

window.show()
app.exec_()

