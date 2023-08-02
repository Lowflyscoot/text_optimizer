import sys
from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)
        self.show()

        self.keywords = {}
        self.words = {}
        self.calculate_processing = False

        self.userTextEdit.textChanged.connect(self.calculate_keywords)
        self.startButton.clicked.connect(self.start_calculating)
        self.resetButton.clicked.connect(self.reset_calculating)

    def reset_calculating(self):
        self.userTextEdit.setText("")
        self.systemTextEdit.setText("")
        self.calculate_processing = False
        self.keywords = {}

    def calculate_keywords(self):
        if self.calculate_processing:
            # берём текст из левого поля
            seo_text = self.userTextEdit.toPlainText().lower()
            responce_text = "required keys:\n"
            # выводим ключевики, вычитая уже введённые слова в счётчик
            for keyword, frequency in self.keywords.items():
                responce_text += f"{keyword} {int(frequency) - seo_text.count(keyword)}\n"

            responce_text += "\nfacted keys:\n"
            self.calculate_words_frequency(seo_text)
            counter = 0
            for word, freq in self.words.items():
                responce_text += f"{word}: {freq}\n"
                counter += 1
                if counter > 10:
                    break

            responce_text += "\n" + self.calculate_text_parameters(seo_text)
            self.systemTextEdit.setText(responce_text)

    def calculate_text_parameters(self, input):
        number_of_words = len(input.split())
        number_of_chars = len(input.replace(" ", ""))
        return f"words: {number_of_words}, char without spaces: {number_of_chars}"

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

    def start_calculating(self):
        if not self.calculate_processing:
            self.calculate_processing = True
            input = self.userTextEdit.toPlainText()
            self.input_parsing(input)
            self.userTextEdit.setText("")

    def input_parsing(self, input):
        input = input.lower()
        for pare in input.split("\n"):
            keyword, frequency = pare.split()
            keyword = keyword.replace("_", " ")
            self.keywords.update({keyword: frequency})


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
