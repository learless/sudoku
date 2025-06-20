import random
import time

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


# горизонтальная линия для поиска
def horizontalLineSelection(matrix: list, lineNumber: int) -> list:
    result = []
    for square in matrix:
        for elem in square[lineNumber]:
            result.append(elem)
    return result


# поиск в вертикальной линии
def searhInVerticalLine(line: list, newElem: str) -> bool:
    for elem in line:
        if elem == newElem:
            # print(line, newElem)
            return True
    return False


# вертикальная линия для поиска
def verticalLineSelection(matrix: list, squareNumber: int, lineNumber: int) -> list:

    if len(matrix) == 1:
        return []
    
    # print(matrix)
    # print(squareNumber, lineNumber)

    # exit()

    result = []
    ''' 
    ( 
    
    [ [[] [] []], [[] [] []], [[] [] []] ] 
    [ [[] [] []], [[] [] []], [[] [] []] ] 
    [ [[] [] []], [[] [] []], [[] [] []] ] 
    
    )

    '''
    for line in matrix[:-1]:
        for squareLine in line[squareNumber]:
            result.append(squareLine[lineNumber])
    return result


# доработать
def printMatrix(matrix: list) -> None:
    print()
    result = []
    _line = []
    for line in matrix:
        if len(line) > 0:
            for miniLine in range(len(line[0])):
                result.append([])
                _line = horizontalLineSelection(line, miniLine)
                for elem in range(len(_line)):
                    result[-1].append(_line[elem])
                    if elem != 0 and (elem + 1) % int(len(_line) ** .5) == 0:
                        result[-1].append('|')
        else:
            return
        result.append([])
        for i in range(len(result[-2])):
            result[-1].append('--')
    
    for line in result:
        for elem in line:
            print(elem, end='\t')
        print()

    print()

# создание матрицы
def createMatrix(rank=4) -> list:

    # 1..9, A..Z, a..z  
    alphabet = [str(number) for number in range(1, 10)] \
        + [chr(letter) for letter in range(65, 91)] \
        + [chr(letter) for letter in range(97, 123)]
    
    alphabet = alphabet[:rank**2]
    #print(alphabet)
    #print()

    '''
    [
    [1, 2, 3]
    [4, 5, 6]
    [7, 8, 9]
    ]
    '''


    checkForRegneration = False

    matrix = []

    for column in range(rank):

        matrix.append([])

        square = 0

        while square < rank:
            if (column + 1 != rank) or (square + 1 != rank):
                matrix[column].append([])
                for i in range(rank):
                    
                    matrix[column][square].append([])
                    
                    for j in range(rank):

                        symbol = random.randint(0, len(alphabet) - 1)

                        # regenirate
                        while searchInSquare(matrix[column][square], alphabet[symbol]) \
                            or searhInHorizontalLine(horizontalLineSelection(matrix[column], i), alphabet[symbol]) \
                            or searhInVerticalLine(verticalLineSelection(matrix, square, j), alphabet[symbol]):
                                
                            haveIAnyElementToAdd = []

                            for elem in alphabet:
                                if not(searchInSquare(matrix[column][square], elem)) \
                                    and not(searhInHorizontalLine(horizontalLineSelection(matrix[column], i), elem)) \
                                    and not(searhInVerticalLine(verticalLineSelection(matrix, square, j), elem)):
                                    haveIAnyElementToAdd.append(elem)

                            if len(haveIAnyElementToAdd) == 0:
                                checkForRegneration = True

                            if checkForRegneration:
                                break

                            symbol = random.randint(0, len(alphabet) - 1)
                        
                        if not(checkForRegneration):
                            matrix[column][square][i].append(alphabet[symbol])
                        
                        else:
                            break
            else:
                #printMatrix(matrix)
                matrix[column].append([])
                for i in range(rank):
                    matrix[column][square].append([])
                    for j in range(rank):
                        for symbol in alphabet:
                            if not(searchInSquare(matrix[column][square], symbol)) \
                                and not(searhInHorizontalLine(horizontalLineSelection(matrix[column], i), symbol)) \
                                and not(searhInVerticalLine(verticalLineSelection(matrix, square, j), symbol)):
                                    matrix[column][square][i].append(symbol)
                                    #print(symbol)
                                    break
                            # else:
                            #     if searchInSquare(matrix[column][square], symbol):
                            #         print(symbol, 'в кв', matrix[column][square], [i,j])
                            #     if searhInHorizontalLine(horizontalLineSelection(matrix[column], i), symbol):
                            #         print(symbol, 'в горизонте', horizontalLineSelection(matrix[column], i), [i,j])
                            #     if searhInVerticalLine(verticalLineSelection(matrix, square, j), symbol):
                            #         print(symbol, 'в вертиале', verticalLineSelection(matrix, square, j), [i,j])
                for line in matrix[column][square]:
                    if len(line) < rank:
                            matrix.pop()
                            matrix.append([])
                            square = -1
                            #printMatrix(matrix)
                            break

            if checkForRegneration:
                checkForRegneration = False
                
                print(column, square)
                
                matrix.pop()

                square = 0

                matrix.append([])
                
                printMatrix(matrix)
                
                #time.sleep(1)
            else:
                print('g', square)
                square += 1


    printMatrix(matrix)

    #print(matrix)

    resultMatrix = []

    for line in matrix:
        for i in range(len(line)):
            resultMatrix.append(horizontalLineSelection(line, i))

    return resultMatrix

if __name__ == '__main__':
    createMatrix(int(input('rank = ')))