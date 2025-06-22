import createMatrix
import createSudoku

m = createMatrix.createMatrix(int(input('Введите размер поля(X на X):')))

sudoku = createSudoku.createSudoku(m, int(input('Введите количество элементов, которые вы хотите удалить:')))

inc: int = 0

while True:
    createSudoku.printSudoku(sudoku, '\t', '*')
    newElem: list[str] = input("el, posY, posX: ").split()
    if (0 < int(newElem[1]) <= len(m) ** 2) and (0 < int(newElem[2]) <= len(m) ** 2):
        if m[int(newElem[1])-1][int(newElem[2])-1] == newElem[0]:
            createSudoku.addElem(sudoku, int(newElem[1])-1, int(newElem[2])-1, newElem[0])
            print("Yes!")
        else:
            print("No!")
            inc += 1
    else:
        print("Incorrect input!")
        print(newElem)
    if createSudoku.countOfZero(sudoku) == 0:
        createSudoku.printSudoku(sudoku)
        print("You are win!")
        print("Количество ошибок:", inc)
        break
