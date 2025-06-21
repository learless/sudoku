data = []
with open('4x4.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()
    print(data)
    i = 1
    result_data = [str(i) + '\n']
    for line in data[:-2]:
        if line == '\n':
            i += 1
            result_data.append(str(i) + '\n')
        else:
            result_data.append(line)
    print(result_data)
    # file.seek(0, 0)
with open('4x4.txt', 'w', encoding='utf-8') as file:
    file.seek(0, 0)
    for line in result_data:
        file.write(line)
    