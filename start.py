import createMatrix
import createSudoku

s = createMatrix.createMatrix(int(input()))

print(createSudoku.createSudoku(s, int(input())))

print(s)
