
def read_input_data(sud_number):
    """ Прочитать Судоку из указанного файла и возвратить судоку в массиве символов исходя из запрощенного номера"""

    sud_box = []
    n = 9  # размер судоку 9х9 значит длина подстроки должна быть 9 символов

    with open('input.txt', 'r', encoding='utf8') as f:
        # формирум массив из строк судоку
        for line in f:
            for i in [line[i:i + n] for i in range(0, len(line) - 1, n)]:  # разбиваем судоку строку по n символов
                sud_box.append([int(ch) for ch in i])  # переводим символы в массив
    # возвращаем судоку в массиве символов исходя из запрощенного номера судоку sud_number
    return sud_box[(sud_number * n - n):sud_number * n]


def solve_recursion(grid, row, col):
    # Проверяем дошли ли до последнего столбца, если не дошли ищем подходящее значение, если дошли проверяем ряд
    if col == 9:
        if row == 8:  # Проверяем дошли ли до последнего ряда, если дошли значит прошли все поле
            return True
        # Если не дошли до последнего ряда увеличиваем ряд на 1 и начинаем проверять опять с 0 столбца
        row += 1
        col = 0
    if grid[row][col] > 0:  # если в текущей позиции не 0 значение, то увеличиваем глубину рекурсии с увеличением столбца
        return solve_recursion(grid, row, col + 1)
    # если в текущей позиции  0 значение, то начинаем подбирать числа для данной позиции
    for number in range(1, 10):
        if check_valid(sudoku_grid, row, col, number):
            # если число подошло ставим его на текущую позицию
            grid[row][col] = number
            #  увеличиваем глубину рекурсии с увеличением столбца, если возвращается True,то прошли все поле
            if solve_recursion(sudoku_grid, row, col + 1):
                return True  # возвращение из рекурсии
        # если число не подошло возвращаем значение 0 в текущую позицию и проверям следующее число
        grid[row][col] = 0
    return False  # решение не найдено


def check_valid(grid, row, col, number):
    """ Прочитать Судоку из массива и текущую позицию с коорд col и row определить валидно ли число number для данной позиции"""

    for i in range(9):
        if grid[row][i] == number:  # проверяем столбцы на существование данного числа number
            return False
    for i in range(9):
        if grid[i][col] == number:  # проверяем ряды на существование данного числа number
            return False
    # проверяем квадрат 3х3 для текущей позиции col и row на существование данного числа number
    sud_square_row = row - row % 3  # находим координаты квадрата
    sud_square_col = col - col % 3 
    for i in range(3):
        for j in range(3):
            if grid[sud_square_row + i][sud_square_col + j] == number:
                return False
    return True


def display_sudoku(grid):
    """ Прочитать Судоку из массива и вывести на дисплей в удобном и читаемом виде"""

    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - - - ")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|  ", end='')
            print(grid[i][j], end="  ")
        print()


if __name__ == '__main__':

    try:
        n = int(input("N: "))
        # очищаем выходной файл
        with open("output.txt", 'w') as f:
            f.close()
        for i in range(1, n + 1):
            sudoku_solved = ''
            sudoku_grid = read_input_data(i)
            print(f"\n Sudoku {i} \n")
            display_sudoku(sudoku_grid)
            if solve_recursion(sudoku_grid, 0, 0):
                print(f"Resolved")
                display_sudoku(sudoku_grid)
                for row in sudoku_grid:
                    for ch in range(len(row)):
                        sudoku_solved = f'{sudoku_solved}{str(row[ch])}'
            else:
                sudoku_solved = "Not resolved"
                print(f"{sudoku_solved}")

            with open('output.txt', 'a') as file:
                file.write(sudoku_solved + '\n')
        sudoku_exit = input("\n Press Enter To Exit...")
    except Exception as e:
        print(f"\n Check input data !!!!\n ERROR: {e}")
