# import sys
# from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QCheckBox,
#                             QPushButton, QMessageBox, QApplication)
# from PyQt5.QtGui import QIcon
# from PyQt5.QtGui import QFont
# from PyQt5.QtCore import Qt

# class AutoWindow(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.showFullScreen()
    
#     def initUI(self):
#         #self.setGeometry(815, 440, 290, 200)
#         self.setWindowTitle('Судоку')
#         self.setWindowIcon(QIcon('icon.ico'))
        
#         self.lbl = QLabel('Авторизация', self)
#         self.lbl.move(30, 10)
#         self.lbl.setFont(QFont("Times New Roman", 22))
        
#         self.login_lbl = QLabel('Логин:', self)
#         self.login_lbl.move(20, 65)
#         self.login_lbl.setFont(QFont("Times New Roman", 13))
        
#         self.login = QLineEdit(self)
#         self.login.move(125, 65)
#         self.login.resize(150, 25)
        
#         self.pass_lbl = QLabel('Пароль:', self)
#         self.pass_lbl.move(20, 110)
#         self.pass_lbl.setFont(QFont("Times New Roman", 13))
        
#         self.password = QLineEdit(self)
#         self.password.move(125, 110)
#         self.password.resize(150, 25)
#         self.password.setEchoMode(QLineEdit.Password)
        
#         auth_btn = QPushButton('Войти', self)
#         auth_btn.move(15, 160)
#         auth_btn.resize(110, 30)
#         auth_btn.clicked.connect(self.check_auth)
        
#         reg_btn = QPushButton('Регистрация', self)
#         reg_btn.move(165, 160)
#         reg_btn.resize(110, 30)
#         reg_btn.clicked.connect(self.show_reg_window)
        
#         self.show()

#     def check_auth(self):
#         with open('authorization.txt', 'r', encoding='utf-8') as authorization:
#             data = authorization.readlines()
            
#             l_p = dict()
#             for line in data:
#                 _login, _password = line.split()
#                 l_p[_login] = _password
            
#             if self.login.text() in l_p.values(): 
#                 if self.password.text() == l_p[self.login.text()]:
#                     self.success = HelloNewWorld()
#                     self.hide()

#                 else:
#                     QMessageBox.warning(self, 'Ошибка!', 'Неправильный пароль!', QMessageBox.Ok)
            
#             else:
#                 QMessageBox.warning(self, 'Ошибка!', 'Не существует аккаунта с таким имением пользователя!', QMessageBox.Ok)
            

   
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = AutoWindow()
#     sys.exit(app.exec_())

from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
    QVBoxLayout)


class Dialog(QDialog):
    NumGridRows = 3
    NumButtons  = 4

    def __init__(self):
        super(Dialog, self).__init__()

        self.createMenu()
        self.createHorizontalGroupBox()
        self.createGridGroupBox()
        self.createFormGroupBox()

        bigEditor = QTextEdit()
        bigEditor.setPlainText(
            "Этот виджет занимает все оставшееся пространство "
            "в макете верхнего уровня."
        )

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(bigEditor)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Basic Layouts")

    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("Horizontal layout")
        layout = QHBoxLayout()

        for i in range(Dialog.NumButtons):
            button = QPushButton("Button %d" % (i + 1))
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    def createGridGroupBox(self):
        self.gridGroupBox = QGroupBox("Grid layout")
        layout = QGridLayout()

        for i in range(Dialog.NumGridRows):
            label = QLabel("Line %d:" % (i + 1))
            lineEdit = QLineEdit()
            layout.addWidget(label,    i + 1, 0)
            layout.addWidget(lineEdit, i + 1, 1)

        self.smallEditor = QTextEdit()
        self.smallEditor.setPlainText(
            "Этот виджет занимает около двух третей "
            "макета сетки. \n Смотрим соотношение `setColumnStretch`!"
        )

        layout.addWidget(self.smallEditor, 0, 2, 5, 1)   # 0, 2, 4, 1

        # QGridLayout.setColumnStretch(column, stretch)
        # Устанавливает растягивающий коэффициент столбца столбца для растягивания. 
        # Первый столбец - номер 0.
        #layout.setColumnStretch(0, 1)      # label
        layout.setColumnStretch(1, 10)      # lineEdit
        layout.setColumnStretch(2, 20)      # smallEditor
        self.gridGroupBox.setLayout(layout)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        layout.addRow(QLabel("Line 1:"), QLineEdit())
        layout.addRow(QLabel("Строка 2, длинный текст:"), QComboBox())
        layout.addRow(QLabel("Line 3:"), QSpinBox())
        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':
    import sys
    app    = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
