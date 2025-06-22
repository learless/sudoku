import random
import createSudoku
import createMatrix
import sys

alphabet = [str(number) for number in range(1, 10)] \
        + [chr(letter) for letter in range(65, 91)] \
        + [chr(letter) for letter in range(97, 123)]

def getSudokuFromFile(rank: int, difficult: str) -> list:
    lines = []

    with open(f'source\\{str(rank)}x{str(rank)}.txt', 'r') as file:
        lines = file.readlines()

    data = dict()
    
    number = 0

    for line in lines:
        line_data = line.strip().split()
        if len(line_data) == 1 and line_data != ['\n']:
            number = int(line_data[0])
            data[number] = []
            continue
        data[number].append(line_data)

    solved_sudoku = data[random.randint(1, len(data))]


    # 4x4 - 105
    # 3x3 - 54/55
    # 2x2 - 11
    difficulties = dict()
    difficulties[2] = {
        'easy': 3,
        'medium': 7,
        'hard': 11
    }
    difficulties[3] = {
        'easy': 15,
        'medium': 35,
        'hard': 50
    }
    difficulties[4] = {
        'easy': 50,
        'medium': 80,
        'hard': 105
    }
    
    sudoku = createSudoku.createSudoku(solved_sudoku, difficulties[rank][difficult])

    return [sudoku, solved_sudoku, alphabet[:rank**2]]

def getSudokuFromGeneration(rank: int, difficult: str) -> list:
    # 4x4 - 105
    # 3x3 - 54/55
    # 2x2 - 11
    difficulties = dict()
    difficulties[2] = {
        'easy': 3,
        'medium': 7,
        'hard': 11
    }
    difficulties[3] = {
        'easy': 15,
        'medium': 35,
        'hard': 50
    }
    difficulties[4] = {
        'easy': 50,
        'medium': 80,
        'hard': 105
    }

    solved_sudoku = createMatrix.createMatrix(rank)
    sudoku = createSudoku.createSudoku(solved_sudoku, difficulties[rank][difficult])

    return [sudoku, solved_sudoku, alphabet[:rank**2]]

if __name__ == '__main__':
    rank = int(input('Введите ранг судоку (2, 3, 4): '))
    difficult = input('Введите сложность (easy, medium, hard): ').lower()
    if '-g' in sys.argv:
        sudoku = getSudokuFromGeneration(rank, difficult)
        createSudoku.printSudoku(sudoku[0])
    else:
        sudoku = getSudokuFromFile(rank, difficult)
        createSudoku.printSudoku(sudoku[0])