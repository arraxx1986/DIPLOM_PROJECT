import os
import functions as f


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(599, 318)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 80, 101, 41))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 241, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 241, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 130, 131, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 180, 131, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 230, 221, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(260, 40, 321, 231))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 599, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Получить SMILES"))
        self.label.setText(_translate("MainWindow", "Название растения"))
        self.pushButton_2.setText(_translate("MainWindow", "Прогноз токсичности"))
        self.pushButton_3.setText(_translate("MainWindow", "Прогноз мишеней"))
        self.pushButton_4.setText(_translate("MainWindow", "Проверка наличия файла SMILES"))

def check_file_SMILES():
    directory = os.getcwd()  # проверяем наличие основного файла с SMILES
    files = os.listdir(directory)
    if 'END_TABLE.xlsx' not in files:
        ui.pushButton.setEnabled(True)
        ui.textBrowser.setText('Файл не найден. В поле введите название растения на латинском языке и нажмите кнопку "Получить SMILES".')
    else:
        ui.pushButton_2.setEnabled(True)
        ui.pushButton_3.setEnabled(True)
        ui.textBrowser.setText('Файл найден. Доступны кнопки для проведения прогноза токсичности и прогноза мишеней.')
def get_SMILES():
    plant_name = ui.lineEdit.text()
    flag = 0
    try:
        driver = f.web_driver()
        f.sdf_download(plant_name, driver)
    except:
        flag = 1
    if flag == 0:
        list_of_smiles = f.smiles_to_xlsx()
    else:
        ui.textBrowser.setText('Для данного растения в базе данных отсутствуют известные вещества')
    f.create_END_TABLE(list_of_smiles)
    ui.textBrowser.setText('в директории с программой создана таблица с данными SMILES. Теперь доступны прогноз токсичности и прогноз мишеней.')

def toxicity():
    try:
        driver = f.web_driver()
        f.toxicity_estimation(driver)
        ui.textBrowser.setText('В директории создан файл с результатами прогноза токсичности')
    except:
        ui.textBrowser.setText('Ошибка сервера. Стоит уменьшить количество запрашиваемых молекул в файле SMILES или попробовать позже.')
def targets():
    try:
        driver = f.web_driver()
        f.total_target_prediction(driver)
        f.total_targets_proved(driver)
        f.targets_calculation(driver)
        ui.textBrowser.setText('В директории создан pdf файл с результатами прогноза, а также таблица с потенциальными мишенями.')
    except:
        ui.textBrowser.setText('Ошибка сервера. Стоит попробовать позже.')
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.pushButton.setEnabled(False)
    ui.pushButton_2.setEnabled(False)
    ui.pushButton_3.setEnabled(False)
    ui.pushButton_4.clicked.connect(check_file_SMILES)
    ui.textBrowser.setText('Проверьте наличие файла SMILES в директории с программой: нажмите соответствующую кнопку.')
    ui.pushButton.clicked.connect(get_SMILES)
    ui.pushButton_2.clicked.connect(toxicity)
    ui.pushButton_3.clicked.connect(targets)

    MainWindow.show()
    sys.exit(app.exec_())
