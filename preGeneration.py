import createMatrix

print('3:')
for i in range(1000):
    with open('3x3.txt', 'r+', encoding='utf-8') as file:
        file.readlines()
        matrix = createMatrix.createMatrix(3)
        for line in matrix:
            for elem in line:
                file.write(elem + ' ')
            file.write('\n')
        file.write('\n')
    print(i,end=' ')

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