import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QCheckBox,
                            QPushButton, QMessageBox, QApplication)
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AutoWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(815, 440, 290, 200)
        self.setWindowTitle('Привет')
        self.setWindowIcon(QIcon('icon.ico'))
        
        self.lbl = QLabel('Авторизация', self)
        self.lbl.move(30, 10)
        self.lbl.setFont(QFont("Times New Roman", 22))
        
        self.login_lbl = QLabel('Логин:', self)
        self.login_lbl.move(20, 65)
        self.login_lbl.setFont(QFont("Times New Roman", 13))
        
        self.login = QLineEdit(self)
        self.login.move(125, 65)
        self.login.resize(150, 25)
        
        self.pass_lbl = QLabel('Пароль:', self)
        self.pass_lbl.move(20, 110)
        self.pass_lbl.setFont(QFont("Times New Roman", 13))
        
        self.password = QLineEdit(self)
        self.password.move(125, 110)
        self.password.resize(150, 25)
        self.password.setEchoMode(QLineEdit.Password)
        
        auth_btn = QPushButton('Войти', self)
        auth_btn.move(15, 160)
        auth_btn.resize(110, 30)
        auth_btn.clicked.connect(self.check_auth)
        
        reg_btn = QPushButton('Регистрация', self)
        reg_btn.move(165, 160)
        reg_btn.resize(110, 30)
        reg_btn.clicked.connect(self.show_reg_window)
        
        self.show()

    def check_auth(self):
        with open('authorization.txt', 'r', encoding='utf-8') as authorization:
            data = authorization.readlines()
            
            l_p = dict()
            for line in data:
                _login, _password = line.split()
                l_p[_login] = _password
            
            if self.login.text() in l_p.values(): 
                if self.password.text() == l_p[self.login.text()]:
                    self.success = HelloNewWorld()
                    self.hide()

                else:
                    QMessageBox.warning(self, 'Ошибка!', 'Неправильный пароль!', QMessageBox.Ok)
            
            else:
                QMessageBox.warning(self, 'Ошибка!', 'Не существует аккаунта с таким имением пользователя!', QMessageBox.Ok)
            
    def show_reg_window(self):
        self.success = RegWindow()

def sokr(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return sokr(a // i, b // i)
    return [a, b]
    
class HelloNewWorld(QWidget):

    mode = True

    def __init__(self):
        super().__init__()
        self.initUI()
            
    def initUI(self):
        self.setGeometry(810, 425, 300, 230)
        self.setWindowTitle('Посчитайка')
        self.setWindowIcon(QIcon('icon.ico'))
        
        self.cb = QCheckBox('Выделение целой части', self)
        self.cb.move(75, 10)
        self.cb.toggle() # галочка
        self.cb.stateChanged.connect(self.changeMyLife)
        
        self.numerator_lbl = QLabel('Числитель:', self)
        self.numerator_lbl.move(10, 50)
        self.numerator_lbl.setFont(QFont("Times New Roman", 12))
        
        self.numerator = QLineEdit(self)
        self.numerator.move(140, 50)
        self.numerator.resize(150, 25)
        
        self.denominator_lbl = QLabel('Знаментатель:', self)
        self.denominator_lbl.move(10, 90)
        self.denominator_lbl.setFont(QFont("Times New Roman", 12))
        
        self.denominator = QLineEdit(self)
        self.denominator.move(140, 90)
        self.denominator.resize(150, 25)

        self.lbl_result = QLabel('Результат:', self)
        self.lbl_result.move(10, 140)
        self.lbl_result.setFont(QFont("Times New Roman", 16))

        self.result_1 = QLineEdit(self)
        self.result_1.move(130, 132)
        self.result_1.resize(40, 50)
        self.result_1.setReadOnly(True)

        self.result_2 = QLineEdit(self)
        self.result_2.move(180, 125)
        self.result_2.resize(110, 25)
        self.result_2.setReadOnly(True)

        self.result_3 = QLineEdit(self)
        self.result_3.move(180, 160)
        self.result_3.resize(110, 25)
        self.result_3.setReadOnly(True)

        justDOIT = QPushButton('Рассчитать', self)
        justDOIT.move(10, 195)
        justDOIT.resize(280, 30)
        justDOIT.clicked.connect(self.calculation)
        
        self.show()

    def changeMyLife(self, state):
        if state == Qt.Checked:
            self.cb.setText('Выделение целой части')
            self.mode = True
            self.result_1.setVisible(True)
            self.result_2.move(180, 125)
            self.result_2.resize(110, 25)
            self.result_3.move(180, 160)
            self.result_3.resize(110, 25)
            if len(self.numerator.text()) > 0 and len(self.denominator.text()) > 0:
                self.calculation()
        else:
            self.cb.setText('Сокращение дробей')
            self.mode = False
            self.result_1.setVisible(False)
            self.result_2.move(145, 125)
            self.result_2.resize(140, 25)
            self.result_3.move(145, 160)
            self.result_3.resize(140, 25)
            if len(self.numerator.text()) > 0 and len(self.denominator.text()) > 0:
                self.calculation()

    def calculation(self):
        if len(self.numerator.text()) == 0 or len(self.denominator.text()) == 0:
            QMessageBox.warning(self, 'Ошибка!', 'Введите данные!', QMessageBox.Ok)
            return

        try:
            int(self.numerator.text().replace(',', '.'))
            if int(self.denominator.text().replace(',', '.')) == 0:
                QMessageBox.warning(self, 'Ошибка!', '0 не может быть в знаменателе!', QMessageBox.Ok)
                return
        except:
            QMessageBox.warning(self, 'Ошибка!', 'Введите целые числа!', QMessageBox.Ok)
            return
        
        if self.mode:
            # Выделение целой части
            self.result_1.setText(str(int(self.numerator.text()) // int(self.denominator.text())))
            self.result_2.setText(str(int(self.numerator.text()) % int(self.denominator.text())))
            self.result_3.setText(self.denominator.text())

        else:
            # Сокращение дробей
            x, y = sokr(int(self.numerator.text()), int(self.denominator.text()))
            self.result_2.setText(str(x))
            self.result_3.setText(str(y))


class RegWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(835, 440, 250, 200)
        self.setWindowTitle('...')
        self.setWindowIcon(QIcon('icon.ico'))
        
        self.lbl = QLabel('Регистрация', self)
        self.lbl.move(35, 10)
        self.lbl.setFont(QFont("Times New Roman", 20))
        
        self.login_lbl = QLabel('Логин:', self)
        self.login_lbl.move(10, 70)
        self.login_lbl.setFont(QFont("Times New Roman", 12))
        
        self.login = QLineEdit(self)
        self.login.move(90, 70)
        self.login.resize(150, 25)
        
        self.pass_lbl = QLabel('Пароль:', self)
        self.pass_lbl.move(10, 110)
        self.pass_lbl.setFont(QFont("Times New Roman", 12))
        
        self.password = QLineEdit(self)
        self.password.move(90, 110)
        self.password.resize(150, 25)
        self.password.setEchoMode(QLineEdit.Password)
        
        reg_btn = QPushButton('Зарегистрироваться', self)
        reg_btn.move(10, 160)
        reg_btn.resize(230, 30)
        reg_btn.clicked.connect(self.reg)
        
        self.show()
    
    def reg(self):
         with open('authorization.txt', 'r+', encoding='utf-8') as authorization:
            data = authorization.readlines()
            
            l_p = dict()
            for line in data:
                _login, _password = line.split()
                l_p[_login] = _password
            
            if self.login.text() not in l_p.values():
                if len(self.login.text()) > 0:
                    if len(self.password.text()) > 7:
                    
                        authorization.write(f'\n{self.login.text()} {self.password.text()}')

                        QMessageBox.information(self, 'Вы зарегистрированы!', 'Регистрация прошла успешно!', QMessageBox.Ok)
                        self.hide()
                
                    else:
                        QMessageBox.warning(self, 'Ошибка!', 'Пароль слишком короткий!', QMessageBox.Ok)
            
                else:
                    QMessageBox.warning(self, 'Ошибка!', 'Введите логин!', QMessageBox.Ok)

            else:
                QMessageBox.warning(self, 'Ошибка!', 'Уже существует аккаунт с таким имением пользователя!', QMessageBox.Ok)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoWindow()
    sys.exit(app.exec_())