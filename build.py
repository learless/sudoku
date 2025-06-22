import os

os.system('nuitka --follow-imports --standalone --jobs=2 --onefile --windows-console-mode=disable --enable-plugin=pyqt5 application.py')