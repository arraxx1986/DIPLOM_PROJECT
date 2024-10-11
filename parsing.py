import sys
from PyQt5.QtWidgets import *

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GUI software')
        self.ledText = QLineEdit('Default Text', self)
        self.resize(300,200)
        self.ledText.move(90,50)
        self.btnupdate = QPushButton('Update Window Title', self)
        self.btnupdate.move(90,100)
        self.btnupdate.clicked.connect(self.evt_btnupdate_clicked)

    def evt_btnupdate_clicked(self):
        self.setWindowTitle()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())









