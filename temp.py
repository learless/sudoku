import random

# посик в квадрате
def searchInSquare(matrix: list, newElem: str) -> bool:
    for line in matrix:
        for elem in line:
            if elem == newElem:
                return True
    return False


# поиск в горизонтальной линии
def searhInHorizontalLine(line: list, newElem: str) -> bool:
    for elem in line:
        if elem == newElem:
            # print(line, newElem)
            return True
    return False


# выбор линии для поиска
def horizontalLineSelection(matrix: list, lineNumber: int) -> list:
    result = []
    for square in matrix:
        for elem in square[lineNumber]:
            result.append(elem)
    return result


# поиск в горизонтальной линии
def searhInVerticalLine(line: list, newElem: str) -> bool:
    for elem in line:
        if elem == newElem:
            # print(line, newElem)
            return True
    return False

# выбор линии для поиска
def verticalLineSelection(matrix: list, lineNumber: int) -> list:
    result = []
    for square in matrix:
        for line in square:
            result.append(line[lineNumber])
    return result


# создание матрицы
def createMatrix(rank=4):

    # 1..9, A..Z, a..z  
    alphabet = [str(number) for number in range(1, 10)] \
        + [chr(letter) for letter in range(65, 91)] \
        + [chr(letter) for letter in range(97, 123)]
    
    alphabet = alphabet[:rank**2]
    print(alphabet)
    print()

    '''
    [
    [1, 2, 3]
    [4, 5, 6]
    [7, 8, 9]
    ]
    '''


    checkForRegneration = False

    matrix = []

    while line:
        matrix.append([])

    square = 0

    while square < rank:
        matrix.append([])
        for i in range(rank):
            
            matrix[square].append([])
            
            for j in range(rank):

                symbol = random.randint(0, len(alphabet) - 1)

                # regenirate
                while searchInSquare(matrix[square], alphabet[symbol]) \
                    or searhInHorizontalLine(horizontalLineSelection(matrix, i), alphabet[symbol]):
                        
                    haveIAnyElementToAdd = []

                    for elem in alphabet:
                        if not(searchInSquare(matrix[square], elem)) \
                            and not(searhInHorizontalLine(horizontalLineSelection(matrix, i), elem)):
                            haveIAnyElementToAdd.append(elem)

                    if len(haveIAnyElementToAdd) == 0:
                        checkForRegneration = True

                    if checkForRegneration:
                        break

                    symbol = random.randint(0, len(alphabet) - 1)
                
                if not(checkForRegneration):
                    matrix[square][i].append(alphabet[symbol])
                
                else:
                    break

        if checkForRegneration:
            checkForRegneration = False
            print(square)
            matrix.pop()
        else:
            print('g', square)
            square += 1

    print()    
    for square in matrix:
        for line in square:
            print(line)
        print()
    print()
    print(matrix)

if __name__ == '__main__':
    createMatrix(int(input('rank = ')))