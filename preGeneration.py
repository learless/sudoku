import createMatrix
import os

os.chdir(os.getcwd() + '\\source')

kol = int(input('kol(2) = '))
print('2:')
for i in range(kol):
    with open('2x2.txt', 'r+', encoding='utf-8') as file:
        file.readlines()
        file.write(f'{str(i+1)}\n')
        matrix = createMatrix.createMatrix(2)
        for line in matrix:
            for elem in line:
                file.write(elem + ' ')
            file.write('\n')
    print(i,end=' ')
print()


kol = int(input('kol(3) = '))
print('3:')
for i in range(kol):
    with open('3x3.txt', 'r+', encoding='utf-8') as file:
        file.readlines()
        matrix = createMatrix.createMatrix(3)
        for line in matrix:
            for elem in line:
                file.write(elem + ' ')
            file.write('\n')
        file.write('\n')
    print(i,end=' ')
print()


kol = int(input('kol(4) = '))
print('4:')
for i in range(50):
    with open('4x4.txt', 'r+', encoding='utf-8') as file:
        file.readlines()
        matrix = createMatrix.createMatrix(4)
        for line in matrix:
            for elem in line:
                file.write(elem + ' ')
            file.write('\n')
        file.write('\n')
    print(i,end=' ')
print()