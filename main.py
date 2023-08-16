import sys
from PyQt5 import QtWidgets, uic
import json


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)
        self.show()

        self.keywords = {}
        self.words = {}
        self.saving_buffer = ""
        self.calculate_processing = False
        self.edit_mode_enable = False

        self.userTextEdit.textChanged.connect(self.calculate_keywords)
        self.startButton.clicked.connect(self.start_calculating)
        self.resetButton.clicked.connect(self.reset_calculating)
        self.editButton.clicked.connect(self.edit_mode)
        self.loadButton.clicked.connect(self.load_keywords)
        self.saveButton.clicked.connect(self.save_keywords)

    def save_keywords(self):
        with open("saved_keys.json", "w") as file:
            json.dump(self.keywords, file)
            # saving_keys = ""
            # for key, freqency in self.keywords.items():
            #     saving_keys += f"{key} {str(freqency)}\n"
            # file.write(saving_keys)

    def load_keywords(self):
        with open("saved_keys.json", "r") as file:
            self.keywords = json.load(file)
            # loaded_keys = file.read()
            # self.keywords = {}
            # self.input_parsing(loaded_keys)
            if not self.calculate_processing:
                self.calculate_processing = True
            self.calculate_keywords()

    def edit_mode(self):
        if not self.edit_mode_enable:
            self.edit_mode_enable = True
            saving_keywords = self.keywords
            self.saving_buffer = self.userTextEdit.toPlainText()
            new_text_buffer = ""
            for key, frequency in saving_keywords.items():
                new_text_buffer += key + " " + str(frequency) + "\n"
            self.reset_calculating()
            self.userTextEdit.setText(new_text_buffer)
        else:
            self.edit_mode_enable = False
            self.start_calculating()
            self.userTextEdit.setText(self.saving_buffer)
            self.saving_buffer = ""

    # обнуление ввода и ключевиков, сброс в исходное состояние
    def reset_calculating(self):
        self.userTextEdit.setText("")
        self.systemTextEdit.setText("")
        self.calculate_processing = False
        self.keywords = {}

    # пересчёт ключевых слов при каждом изменении ввода
    def calculate_keywords(self):
        if self.calculate_processing:
            # берём текст из левого поля
            seo_text = self.userTextEdit.toPlainText().lower()
            # если встречается стоп - дальше не учитываем
            if "stop" in seo_text:
                seo_text = seo_text[:seo_text.find("stop")]
            responce_text = "required keys:\n"
            # выводим ключевики, вычитая уже введённые слова в счётчик
            for keyword, frequency in self.keywords.items():
                responce_text += f"{keyword} {int(frequency) - seo_text.count(keyword)}\n"

            # пока частотность определяется строго - оно бесполезно, надо доделать
            # responce_text += "\nfacted keys:\n"
            # self.calculate_words_frequency(seo_text)

            # выводим первые 10 самых частых слов
            # counter = 0
            # for word, freq in self.words.items():
            #     responce_text += f"{word}: {freq}\n"
            #     counter += 1
            #     if counter > 10:
            #         break

            # дописываем длину текста и выводим
            responce_text += "\n" + self.calculate_text_parameters(seo_text)
            self.systemTextEdit.setText(responce_text)

    # определение длины текста в символах и словах
    def calculate_text_parameters(self, input):
        number_of_words = len(input.split())
        number_of_chars = len(input.replace(" ", ""))
        return f"words: {number_of_words}, char without spaces: {number_of_chars}"

    # определяем частотность всех слов в тексте
    def calculate_words_frequency(self, input):
        text_buf = input.replace(",", "")
        text_buf = text_buf.replace(".", "")
        text_buf = text_buf.split()
        self.words = {}
        tmp_words = {}
        for word in text_buf:
            if word in self.words.keys():
                self.words[word] += 1
            else:
                self.words.update({word: 1})

        sorted_keys = sorted(self.words, key=self.words.get, reverse=True)

        for key in sorted_keys:
            if len(key) > 4:
                tmp_words.update({key: self.words[key]})

        self.words = tmp_words

    # запуск расчёта, ввод разбирается на слова и программа переходит в рабочий режим по нажатию на кнопку
    def start_calculating(self):
        if not self.calculate_processing:
            self.calculate_processing = True
            input = self.userTextEdit.toPlainText()
            self.input_parsing(input)
            self.userTextEdit.setText("")

    # парсинг вошедшей строки
    def input_parsing(self, input):
        input = input.lower()
        for string in input.split("\n"):
            # строки с менее чем 2 элементами игнорируем
            if len(string.split(" ")) < 2:
                continue
            frequency = 0
            keyword = ""
            # Перебираем ввод с конца в поисках первого числа
            for word in reversed(string.split()):
                if frequency == 0:
                    if word.isdigit():
                        frequency = int(word)
                        break
            # Если нашли в строке ненулевое число нужного количества вхождений - формируем ключевик
            if frequency > 0:
                keyword = string[:keyword.find(str(frequency)) - 1].rstrip()
                self.keywords.update({keyword: frequency})


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
