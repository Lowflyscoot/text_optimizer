import sys
from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)
        self.show()

        self.keywords = {}
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
            seo_text = self.userTextEdit.toPlainText()
            responce_text = ""
            for keyword, frequency in self.keywords.items():
                responce_text += f"{keyword} {int(frequency) - seo_text.count(keyword)}\n"
            self.systemTextEdit.setText(responce_text)

    def start_calculating(self):
        if not self.calculate_processing:
            self.calculate_processing = True
            input = self.userTextEdit.toPlainText()
            self.input_parsing(input)
            self.userTextEdit.setText("")

    def input_parsing(self, input):
        for pare in input.split("\n"):
            keyword, frequency = pare.split()
            keyword = keyword.replace("_", " ")
            self.keywords.update({keyword: frequency})


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
