import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QComboBox, QHBoxLayout, QGridLayout, QLineEdit
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from getSudoku import getSudokuFromFile, alphabet

class SudokuFieldScreen(QWidget):
    def __init__(self, size_text, difficult="easy", stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        # Таймер
        self.start_time = time.time()

        # Определяем размер поля
        size_map = {"2x2": 4, "3x3": 9, "4x4": 16}
        grid_size = size_map.get(size_text, 4)
        block_size = int(grid_size ** 0.5)

        # Получаем данные судоку
        rank = block_size
        sudoku_data = getSudokuFromFile(rank, difficult)
        sudoku = sudoku_data[0]
        solved_sudoku = sudoku_data[1]
        allowed_alphabet = sudoku_data[2]
        self.solved_sudoku = solved_sudoku  # <--- добавьте эту строку

        # Создаём валидатор для разрешённых символов
        regexp = QRegExp(f"[{''.join(allowed_alphabet)}]")
        validator = QRegExpValidator(regexp)

        grid_layout = QGridLayout()

        # Получаем размер экрана для адаптации размеров
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        min_side = min(screen_size.width(), screen_size.height())
        cell_size = int(min_side * 0.7 // grid_size)

        # Счётчик ошибок
        self.errors = 0
        self.error_label = QLabel("Ошибки: 0")
        self.error_label.setFont(QFont("Arial", int(cell_size * 0.25)))
        layout.addWidget(self.error_label, alignment=Qt.AlignRight)

        # Контейнер для поля с границей
        field_container = QWidget()
        field_container.setStyleSheet("QWidget { border: 2px solid #888; border-radius: 6px; }")
        field_container_layout = QVBoxLayout()
        field_container_layout.setContentsMargins(16, 16, 16, 16)
        field_container_layout.addLayout(grid_layout)
        field_container.setLayout(field_container_layout)

        # Для любого размера делаем визуальное разделение на блоки-виджеты
        block_widgets = [[QWidget() for _ in range(block_size)] for _ in range(block_size)]
        block_layouts = [[QGridLayout() for _ in range(block_size)] for _ in range(block_size)]
        for br in range(block_size):
            for bc in range(block_size):
                block_widgets[br][bc].setStyleSheet("QWidget { border: 2px solid #888; border-radius: 6px; }")
                block_layouts[br][bc].setSpacing(4)
                block_widgets[br][bc].setLayout(block_layouts[br][bc])
                grid_layout.addWidget(block_widgets[br][bc], br, bc)

        # Заполняем поле судоку
        self.cells = []
        for row in range(grid_size):
            row_cells = []
            for col in range(grid_size):
                cell = QLineEdit()
                cell.setFixedSize(cell_size, cell_size)
                cell.setAlignment(Qt.AlignCenter)
                cell.setFont(QFont("Arial", int(cell_size * 0.4)))
                cell.setMaxLength(2 if grid_size > 9 else 1)
                cell.setValidator(validator)
                br = row // block_size
                bc = col // block_size
                value = sudoku[row][col] if row < len(sudoku) and col < len(sudoku[row]) else "0"
                solution = solved_sudoku[row][col] if row < len(solved_sudoku) and col < len(solved_sudoku[row]) else "0"
                if value != "0":
                    cell.setText(value)
                    cell.setReadOnly(True)
                    cell.setStyleSheet("background-color: #e0e0e0;")
                else:
                    # Проверка правильности ввода
                    def make_check(cell, row=row, col=col, solution=solution):
                        def check():
                            text = cell.text()
                            if text == "":
                                cell.setStyleSheet("")
                                return
                            if text == solution:
                                cell.setStyleSheet("background-color: #c8e6c9;")  # зелёный
                            else:
                                cell.setStyleSheet("background-color: #ffcdd2;")  # красный
                                self.errors += 1
                                self.error_label.setText(f"Ошибки: {self.errors}")
                            self.check_win()
                        return check
                    cell.textChanged.connect(make_check(cell))
                block_layouts[br][bc].addWidget(cell, row % block_size, col % block_size)
                row_cells.append(cell)
            self.cells.append(row_cells)

        layout.addWidget(field_container)
        self.setLayout(layout)

    def check_win(self):
        # Проверяем, что все значения совпадают с решением
        for row, row_cells in enumerate(self.cells):
            for col, cell in enumerate(row_cells):
                if not cell.isReadOnly():
                    # Получаем правильное значение из решённого судоку
                    correct_value = self.solved_sudoku[row][col]
                    if cell.text() != correct_value:
                        return
        # Если все поля заполнены верно
        self.show_result()

    def show_result(self):
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        result_screen = ResultScreen(self.errors, minutes, seconds, self.stacked_widget)
        self.stacked_widget.addWidget(result_screen)
        self.stacked_widget.setCurrentWidget(result_screen)

class ResultScreen(QWidget):
    def __init__(self, errors, minutes, seconds, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        result_label = QLabel(f"Поздравляем!\nВы решили судоку.")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setFont(QFont("Arial", 32))
        layout.addWidget(result_label)

        time_label = QLabel(f"Время: {minutes:02}:{seconds:02}")
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setFont(QFont("Arial", 24))
        layout.addWidget(time_label)

        error_label = QLabel(f"Ошибки: {errors}")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setFont(QFont("Arial", 24))
        layout.addWidget(error_label)

        again_btn = QPushButton("Сыграть ещё раз")
        again_btn.setFont(QFont("Arial", 20))
        again_btn.setStyleSheet("background-color: green; color: white;")
        again_btn.setFixedHeight(80)
        again_btn.clicked.connect(self.back_to_menu)
        layout.addWidget(again_btn)

        self.setLayout(layout)

    def back_to_menu(self):
        self.stacked_widget.setCurrentIndex(1)  # Переход на экран выбора параметров

class GameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        # Получаем размер экрана для адаптации размеров
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        min_side = min(screen_size.width(), screen_size.height())
        btn_width = int(screen_size.width() * 0.32)
        btn_height = int(screen_size.height() * 0.12)
        font_size = int(btn_height * 0.4)
        label_font_size = int(btn_height * 0.5)

        # Заголовок
        label = QLabel("Выберете параметры игры")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", label_font_size))
        layout.addWidget(label)
        layout.addSpacing(int(btn_height * 0.3))  # Добавляем пространство после заголовка

        # Выбор размера судоку (кнопки)
        size_label = QLabel("Размер судоку:")
        size_label.setFont(QFont("Arial", label_font_size))
        layout.addWidget(size_label)
        layout.addSpacing(int(btn_height * 0.2))  # Добавляем пространство после "Размер судоку:"

        self.size_buttons = []
        self.selected_size = "2x2"
        size_btns_container = QWidget()
        size_btn_layout = QHBoxLayout()
        size_btn_layout.setContentsMargins(4, 4, 4, 4)
        size_btn_layout.setSpacing(8)
        for size in ["2x2", "3x3", "4x4"]:
            btn = QPushButton(size)
            btn.setCheckable(True)
            btn.setFont(QFont("Arial", font_size))
            btn.setFixedSize(btn_width, btn_height)
            btn.clicked.connect(self.make_size_handler(btn))
            size_btn_layout.addWidget(btn)
            self.size_buttons.append(btn)
            if size == self.selected_size:
                btn.setChecked(True)
        size_btns_container.setLayout(size_btn_layout)
        size_btns_container.setStyleSheet("")
        layout.addWidget(size_btns_container)
        layout.addSpacing(int(btn_height * 0.3))  # Добавляем пространство после блока кнопок размера

        # Выбор сложности (кнопки)
        diff_label = QLabel("Сложность:")
        diff_label.setFont(QFont("Arial", label_font_size))
        layout.addWidget(diff_label)
        layout.addSpacing(int(btn_height * 0.2))  # Добавляем пространство после "Сложность:"

        self.diff_buttons = []
        self.selected_diff = "Лёгкая"
        diff_btns_container = QWidget()
        diff_btn_layout = QHBoxLayout()
        diff_btn_layout.setContentsMargins(4, 4, 4, 4)
        diff_btn_layout.setSpacing(8)
        for diff in ["Лёгкая", "Средняя", "Сложная"]:
            btn = QPushButton(diff)
            btn.setCheckable(True)
            btn.setFont(QFont("Arial", font_size))
            btn.setFixedSize(btn_width, btn_height)
            btn.clicked.connect(self.make_diff_handler(btn))
            diff_btn_layout.addWidget(btn)
            self.diff_buttons.append(btn)
            if diff == self.selected_diff:
                btn.setChecked(True)
        diff_btns_container.setLayout(diff_btn_layout)
        diff_btns_container.setStyleSheet("")
        layout.addWidget(diff_btns_container)

        # Добавляем пространство перед кнопкой "Играть"
        layout.addSpacing(btn_height // 2)

        # Кнопка начать игру
        play_btn = QPushButton("Играть")
        play_btn.setStyleSheet("background-color: blue; color: white;")
        play_btn.setFont(QFont("Arial", font_size))
        play_btn.setFixedSize((btn_width + 15) * 3, btn_height)
        play_btn.setCursor(Qt.PointingHandCursor)
        play_btn.clicked.connect(self.start_sudoku_field)
        layout.addWidget(play_btn)

        self.setLayout(layout)

    def make_size_handler(self, btn):
        def handler():
            for b in self.size_buttons:
                b.setChecked(False)
            btn.setChecked(True)
            self.selected_size = btn.text()
        return handler

    def make_diff_handler(self, btn):
        def handler():
            for b in self.diff_buttons:
                b.setChecked(False)
            btn.setChecked(True)
            self.selected_diff = btn.text()
        return handler

    def start_sudoku_field(self):
        # Преобразуем сложность из русского в английский
        diff_map = {
            "Лёгкая": "easy",
            "Средняя": "medium",
            "Сложная": "hard"
        }
        diff_eng = diff_map.get(self.selected_diff, "easy")
        sudoku_field_screen = SudokuFieldScreen(
            self.selected_size,
            diff_eng,                # <-- теперь на английском
            self.stacked_widget
        )
        self.stacked_widget.addWidget(sudoku_field_screen)
        self.stacked_widget.setCurrentWidget(sudoku_field_screen)

class StartScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Судоку")
        self.setWindowIcon(QIcon("source/icon.ico"))  # Путь к иконке обновлён

        # Получаем размер экрана для адаптации размеров
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        min_side = min(screen_size.width(), screen_size.height())
        btn_width = int(screen_size.width() * 0.99)
        btn_height = int(screen_size.height() * 0.2)
        font_size = int(btn_height * 0.4)
        title_font_size = int(btn_height * 0.5)

        layout = QVBoxLayout()

        title = QLabel("Добро пожаловать в Судоку!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: {title_font_size}px; font-weight: bold;")
        layout.addWidget(title)

        start_btn = QPushButton("Начать игру")
        start_btn.setStyleSheet("background-color: green; color: white;")
        start_btn.setToolTip("Нажмите, чтобы начать игру")
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.setFixedSize(btn_width, btn_height)
        start_btn.setFont(QFont("Arial", font_size))
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn)

        exit_btn = QPushButton("Выйти")
        exit_btn.setStyleSheet("background-color: red; color: white;")
        exit_btn.setToolTip("Закрыть приложение")
        exit_btn.setCursor(Qt.PointingHandCursor)
        exit_btn.setFixedSize(btn_width, btn_height)
        exit_btn.setFont(QFont("Arial", font_size))
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)

        self.setLayout(layout)

    def start_game(self):
        self.stacked_widget.setCurrentIndex(1)  # Переключаемся на экран выбора

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()

    start_screen = StartScreen(stacked_widget)
    game_screen = GameScreen(stacked_widget)

    stacked_widget.addWidget(start_screen)  # индекс 0
    stacked_widget.addWidget(game_screen)   # индекс 1

    stacked_widget.showMaximized()  # Открываем окно во весь экран

    sys.exit(app.exec_())