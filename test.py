import sys
from PyQt5.QtWidgets import *
#
# app = QApplication(sys.argv)
# dlgMain = QDialog()
# dlgMain.setWindowTitle('First GUI')
# dlgMain.show()
# sys.exit(app.exec_())
class DlMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Second GUI')
        self.leadText = QLineEdit('Default Text', self)
        self.leadText.move(100,50)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlgMain = DlMain()
    dlgMain.show()
    sys.exit(app.exec_())