import random
from copy import deepcopy
import time
sss = []

# difficult - количество удаляемых ячеек
def createSudoku(matrix: list[list[str]], difficult = 30) -> list:

    global sss

    de = set()

    global solves

    sss=matrix

    sudoku = deepcopy(matrix)

    deleteElement = 0
    while deleteElement < difficult:

        #print("hello")

        i, j = random.randint(0, len(matrix) - 1), random.randint(0, len(matrix) - 1)

        # i, j
        if sudoku[i][j] == "0":
            continue

        status = deleteElementsFromMatrix(sudoku, i, j)
        if status[0]:
            sudoku = status[1]
            deleteElement += 1
        elif deleteElement not in de:
            time.sleep(0.1)
            print(deleteElement)
            de.add(deleteElement)

    return sudoku
# 4x4 - 109
# 3x3 - 54/55
# 2x2 - 11

def columnCheck(newElement: str, matrix: list[list[str]], column: int) -> bool:
    for row in matrix:
        if row[column] == newElement:
            return False
    return True

def check(newElement: str, matrix: list[list[str]], row: int, column: int) -> bool:

    if ''.join(matrix[row]).find(newElement) == -1 \
    and columnCheck(newElement, matrix, column):
        squareY: int = int((row // int(len(matrix) ** .5)) * (len(matrix) ** .5))
        squareX: int = int((column // int(len(matrix) ** .5)) * (len(matrix) ** .5))
        squareElements = []
        for squareRow in range(int(len(matrix) ** .5)):
            for squareColumn in range(int(len(matrix) ** .5)):
                squareElements.append(matrix[squareY + squareRow][squareX + squareColumn])
        if newElement in squareElements:
            return False
        else:
            return True
    else:
        return False



def deleteElementsFromMatrix(sudoku: list[list[str]], row: int, column: int) -> list:

    _sudoku = deepcopy(sudoku)

    _sudoku[row][column] = "0"

    coords = []

    for i, line in enumerate(_sudoku):
        if ''.join(line).find("0") != -1:
            coords = [i, ''.join(line).find("0")]
            break

    if countOfSolveSudoku(_sudoku) == 1:
        return [True, _sudoku]
    else:
        #print(solves)
        #(sudoku)
        return [False, _sudoku]

    # if coords == []:
    #     return sudoku



solves = []

def solveSudoku(sudoku: list[list[str]]):

    global solves

    coords = []

    for i, line in enumerate(sudoku):
        if ''.join(line).find("0") != -1:
            coords = [i, ''.join(line).find("0")]
            break

    #print(coords)
    if coords == []:
        solves.append(sudoku)
        return
    #else:
        #print(coords)
        #print(sudoku)
    #time.sleep(2)

    alphabet = [str(number) for number in range(1, 10)] \
        + [chr(letter) for letter in range(65, 91)] \
        + [chr(letter) for letter in range(97, 123)]

    alphabet = alphabet[:len(sudoku[0])]

    for symbol in alphabet:

        if check(newElement=symbol, matrix=sudoku, row=coords[0], column=coords[1]):

            newLine = []
            for j in range(len(sudoku)):
                if j != coords[1]:
                    newLine.append(sudoku[coords[0]][j])
                else:
                    newLine.append(symbol)

            newSudoku = []
            for i in range(len(sudoku)):
                if i != coords[0]:
                    newSudoku.append(sudoku[i])
                else:
                    newSudoku.append(newLine)

            solveSudoku(newSudoku)



def countOfSolveSudoku(sudoku: list[list[str]]) -> int:

    global solves

    solves = []

    solveSudoku(sudoku)

    return len(solves)


def printSudoku(sudoku: list[list[str]], separator: str = '\t', zero: str = "0") -> None:
    print()
    result: list[list[str]] = []

    for i, line in enumerate(sudoku):
        result.append([])
        for elem in range(len(line)):
            if line[elem] != "0":
                result[-1].append(line[elem])
            else:
                result[-1].append(zero)
            if elem != 0 and (elem + 1) % int(len(line) ** .5) == 0 and elem + 1 != len(line):
                result[-1].append('|')
        if (i + 1) % int(len(sudoku) ** .5) == False:
            result.append([])
            for elem in range(len(result[-2])):
                result[-1].append("--")

    for line in result:
        for elem in line:
            print(elem, end=separator)
        print()

    print()

def addElem(matrix: list[list[str]], row: int, column: int, newElem: str) -> None:
    matrix[row][column] = newElem

def countOfZero(matrix: list[list[str]]) -> int:
    result: int = 0
    for line in matrix:
        for elem in line:
            if elem == "0":
                result += 1
    return result
