import sys
import time
import json
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QGridLayout, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QFont, QRegularExpressionValidator
from getSudoku import getSudokuFromFile, alphabet

BEST_RESULTS_FILE = "best_results.json"

def load_best_results():
    if os.path.exists(BEST_RESULTS_FILE):
        with open(BEST_RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_best_result(size_text, difficult, minutes, seconds, errors, hints_used):
    results = load_best_results()
    key = f"{size_text}_{difficult}"
    new_time = minutes * 60 + seconds
    if (
        key not in results or
        new_time < results[key]["time"] or
        (new_time == results[key]["time"] and errors < results[key]["errors"])
    ):
        results[key] = {
            "time": new_time,
            "minutes": minutes,
            "seconds": seconds,
            "errors": errors,
            "hints_used": hints_used
        }
        with open(BEST_RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

class SudokuFieldScreen(QWidget):
    def __init__(self, size_text, difficult="easy", stacked_widget=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.difficult = difficult
        self.size_text = size_text
        self.hints_used = 0
        layout = QVBoxLayout()

        self.start_time = time.time()

        size_map = {"2x2": 4, "3x3": 9, "4x4": 16}
        grid_size = size_map.get(size_text, 4)
        block_size = int(grid_size ** 0.5)

        rank = block_size
        sudoku_data = getSudokuFromFile(rank, difficult)
        sudoku = sudoku_data[0]
        solved_sudoku = sudoku_data[1]
        allowed_alphabet = sudoku_data[2]
        self.solved_sudoku = solved_sudoku

        regexp = QRegularExpression(f"[{''.join(allowed_alphabet)}]")
        validator = QRegularExpressionValidator(regexp)

        grid_layout = QGridLayout()

        # Универсальные размеры для Android
        cell_size = 60

        self.errors = 0
        self.error_label = QLabel("Ошибки: 0")
        self.error_label.setFont(QFont("Arial", 18))

        hint_btn = QPushButton("Подсказка")
        hint_btn.setFont(QFont("Arial", 14))
        hint_btn.setMinimumHeight(40)
        hint_btn.clicked.connect(self.show_hint)

        top_panel = QHBoxLayout()
        top_panel.addWidget(self.error_label, alignment=Qt.AlignRight)
        top_panel.addWidget(hint_btn, alignment=Qt.AlignRight)
        layout.addLayout(top_panel)

        field_container = QWidget()
        field_container.setStyleSheet("QWidget { border: 2px solid #888; border-radius: 6px; }")
        field_container_layout = QVBoxLayout()
        field_container_layout.setContentsMargins(8, 8, 8, 8)
        field_container_layout.addLayout(grid_layout)
        field_container.setLayout(field_container_layout)

        block_widgets = [[QWidget() for _ in range(block_size)] for _ in range(block_size)]
        block_layouts = [[QGridLayout() for _ in range(block_size)] for _ in range(block_size)]
        for br in range(block_size):
            for bc in range(block_size):
                block_widgets[br][bc].setStyleSheet("QWidget { border: 2px solid #888; border-radius: 6px; }")
                block_layouts[br][bc].setSpacing(2)
                block_widgets[br][bc].setLayout(block_layouts[br][bc])
                grid_layout.addWidget(block_widgets[br][bc], br, bc)

        self.cells = []
        for row in range(grid_size):
            row_cells = []
            for col in range(grid_size):
                cell = QLineEdit()
                cell.setFixedSize(cell_size, cell_size)
                cell.setAlignment(Qt.AlignCenter)
                cell.setFont(QFont("Arial", 20))
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
        result_screen = ResultScreen(
            self.errors,
            minutes,
            seconds,
            self.stacked_widget,
            self.size_text,
            self.difficult,
            self.hints_used
        )
        self.stacked_widget.addWidget(result_screen)
        self.stacked_widget.setCurrentWidget(result_screen)

    def show_hint(self):
        # Находит первую пустую ячейку и подставляет правильное значение
        for row, row_cells in enumerate(self.cells):
            for col, cell in enumerate(row_cells):
                if not cell.isReadOnly() and cell.text() == "":
                    correct_value = self.solved_sudoku[row][col]
                    cell.setText(correct_value)
                    cell.setStyleSheet("background-color: #fff9c4;")  # жёлтый для подсказки
                    self.hints_used += 1
                    return

class StartScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Судоку")

        layout = QVBoxLayout()

        title = QLabel("Добро пожаловать в Судоку!")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 28))
        layout.addWidget(title)

        start_btn = QPushButton("Начать игру")
        start_btn.setStyleSheet("background-color: green; color: white;")
        start_btn.setMinimumHeight(80)
        start_btn.setFont(QFont("Arial", 22))
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn)

        best_btn = QPushButton("Лучшие результаты")
        best_btn.setStyleSheet("background-color: orange; color: white;")
        best_btn.setMinimumHeight(80)
        best_btn.setFont(QFont("Arial", 22))
        best_btn.clicked.connect(self.show_best_results)
        layout.addWidget(best_btn)

        exit_btn = QPushButton("Выйти")
        exit_btn.setStyleSheet("background-color: red; color: white;")
        exit_btn.setMinimumHeight(80)
        exit_btn.setFont(QFont("Arial", 22))
        exit_btn.clicked.connect(QApplication.quit)
        layout.addWidget(exit_btn)

        self.setLayout(layout)

    def start_game(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_best_results(self):
        results = load_best_results()
        if not results:
            msg = "Пока нет сохранённых результатов."
        else:
            msg = "Лучшие результаты:\n"
            msg_no_hints = "\nРезультаты без использования подсказок:\n"
            found_no_hints = False
            for key, val in results.items():
                size, diff = key.split("_")
                msg += (
                    f"\nРазмер: {size}, Сложность: {diff.capitalize()}\n"
                    f"Время: {val['minutes']:02}:{val['seconds']:02}, "
                    f"Ошибки: {val['errors']}, Подсказки: {val['hints_used']}\n"
                )
                if val.get("hints_used", 0) == 0:
                    found_no_hints = True
                    msg_no_hints += (
                        f"\nРазмер: {size}, Сложность: {diff.capitalize()}\n"
                        f"Время: {val['minutes']:02}:{val['seconds']:02}, "
                        f"Ошибки: {val['errors']}\n"
                    )
            if not found_no_hints:
                msg_no_hints += "\nНет результатов без подсказок."
            msg += msg_no_hints
        QMessageBox.information(self, "Лучшие результаты", msg)

class ResultScreen(QWidget):
    def __init__(self, errors, minutes, seconds, stacked_widget, size_text, difficult, hints_used):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        result_label = QLabel(f"Поздравляем!\nВы решили судоку.")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setFont(QFont("Arial", 28))
        layout.addWidget(result_label)

        level_label = QLabel(f"Размер: {size_text}, Сложность: {difficult.capitalize()}")
        level_label.setAlignment(Qt.AlignCenter)
        level_label.setFont(QFont("Arial", 20))
        layout.addWidget(level_label)

        time_label = QLabel(f"Время: {minutes:02}:{seconds:02}")
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setFont(QFont("Arial", 18))
        layout.addWidget(time_label)

        error_label = QLabel(f"Ошибки: {errors}")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setFont(QFont("Arial", 18))
        layout.addWidget(error_label)

        hint_label = QLabel(f"Использовано подсказок: {hints_used}")
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setFont(QFont("Arial", 18))
        layout.addWidget(hint_label)

        save_best_result(size_text, difficult, minutes, seconds, errors, hints_used)

        again_btn = QPushButton("Сыграть ещё раз")
        again_btn.setFont(QFont("Arial", 18))
        again_btn.setStyleSheet("background-color: green; color: white;")
        again_btn.setMinimumHeight(60)
        again_btn.clicked.connect(self.back_to_start)
        layout.addWidget(again_btn)

        self.setLayout(layout)

    def back_to_start(self):
        self.stacked_widget.setCurrentIndex(0)

class GameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        label = QLabel("Выберете параметры игры")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 22))
        layout.addWidget(label)
        layout.addSpacing(30)

        size_label = QLabel("Размер судоку:")
        size_label.setFont(QFont("Arial", 20))
        layout.addWidget(size_label)
        layout.addSpacing(15)

        self.size_buttons = []
        self.selected_size = "2x2"
        size_btns_container = QWidget()
        size_btn_layout = QHBoxLayout()
        size_btn_layout.setSpacing(8)
        for size in ["2x2", "3x3", "4x4"]:
            btn = QPushButton(size)
            btn.setCheckable(True)
            btn.setFont(QFont("Arial", 18))
            btn.setMinimumHeight(60)
            btn.clicked.connect(self.make_size_handler(btn))
            size_btn_layout.addWidget(btn)
            self.size_buttons.append(btn)
            if size == self.selected_size:
                btn.setChecked(True)
        size_btns_container.setLayout(size_btn_layout)
        layout.addWidget(size_btns_container)
        layout.addSpacing(20)

        diff_label = QLabel("Сложность:")
        diff_label.setFont(QFont("Arial", 20))
        layout.addWidget(diff_label)
        layout.addSpacing(15)

        self.diff_buttons = []
        self.selected_diff = "Лёгкая"
        diff_btns_container = QWidget()
        diff_btn_layout = QHBoxLayout()
        diff_btn_layout.setSpacing(8)
        for diff in ["Лёгкая", "Средняя", "Сложная"]:
            btn = QPushButton(diff)
            btn.setCheckable(True)
            btn.setFont(QFont("Arial", 18))
            btn.setMinimumHeight(60)
            btn.clicked.connect(self.make_diff_handler(btn))
            diff_btn_layout.addWidget(btn)
            self.diff_buttons.append(btn)
            if diff == self.selected_diff:
                btn.setChecked(True)
        diff_btns_container.setLayout(diff_btn_layout)
        layout.addWidget(diff_btns_container)

        layout.addSpacing(30)

        play_btn = QPushButton("Играть")
        play_btn.setStyleSheet("background-color: blue; color: white;")
        play_btn.setFont(QFont("Arial", 20))
        play_btn.setMinimumHeight(70)
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
        diff_map = {
            "Лёгкая": "easy",
            "Средняя": "medium",
            "Сложная": "hard"
        }
        diff_eng = diff_map.get(self.selected_diff, "easy")
        sudoku_field_screen = SudokuFieldScreen(
            self.selected_size,
            diff_eng,
            self.stacked_widget
        )
        self.stacked_widget.addWidget(sudoku_field_screen)
        self.stacked_widget.setCurrentWidget(sudoku_field_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()

    start_screen = StartScreen(stacked_widget)
    game_screen = GameScreen(stacked_widget)

    stacked_widget.addWidget(start_screen)
    stacked_widget.addWidget(game_screen)

    stacked_widget.showMaximized()

    app.exec()