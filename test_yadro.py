import sys

def csv_loader(filename):
    '''
    Загрузка таблицы в формате .csv
    '''
    with open(filename, 'r') as f:
        table = []
        for line in f:
            words = line.strip().split(',')
            table.append(words)
    return table

def show_csv(table):
    '''
    Отображение таблицы в консоль в формате .csv
    '''
    for i in range(len(table)):
        print(*table[i], sep=',')

def address_checker(table):
    '''
    Проверка корректности названия полей и номеров строк таблицы
    '''
    err_message = ''
    for index in range(1, len(table)):
        if not table[index][0].isdigit():
            err_message = 'Wrong row number ' + table[index][0]
            return err_message
    for col_name in range(1, len(table[0])):
        if not table[0][col_name].isalpha():
            err_message = 'Wrong column name ' + table[0][col_name]
            return err_message

def get_address_from_operand(arg):
    '''
    Раскладывает операнд на имя столбца и номер строки для доступа к 
    соответствующей ячейке таблицы
    arg - операнд в формате *имя столбца**номер строки* (A1, Cell30, etc.)
    Возвращаемые значения: column - имя столбца, row - номер строки
    -----
    Notice: если операнд невозможно разложить, возвращает None, None
    '''
    column = ''
    row = 0
    idx = 0
    if len(arg) > 1 and not arg.isalpha() and arg[0].isalpha():
        while arg[idx].isalpha():
            column += arg[idx]
            idx += 1
        try:
            row = int(arg[idx:])
            return column, row
        except:
            pass
    return None, None

def get_int_from_expr(arg, table):
    '''
    Проверяет, существует ли ячейка по адресу arg в таблице, 
    и возвращает значение этой ячейки (целое число)
    '''
    arg_int = None
    if arg.isdigit():
        arg_int = int(arg)
    else:
        arg_column, arg_row = get_address_from_operand(arg)
        if not (arg_column and arg_row):
            return None
        for i in range(1, len(table[0])):
            if table[0][i] == arg_column:
                for j in range(1, len(table)):
                    if table[j][0] == str(arg_row):
                        arg_int = int(table[j][i])
                        return arg_int
    return arg_int

def compute_expression(expr, table):
    '''
    Вычисление табличных выражений
    '''
    result = 0
    first_int = 0
    second_int = 0
    operand = ''
    if '+' in expr:
        args = expr.split('+', maxsplit = 1)
        operand = '+'
    elif '*' in expr:
        args = expr.split('*', maxsplit = 1)
        operand = '*'
    elif '-' in expr:
        args = expr.split('-', maxsplit = 1)
        operand = '-'
    elif '/' in expr:
        args = expr.split('/', maxsplit = 1)
        operand = '/'
    else:
        return 'Arithmetic operation is missing'
    if args[1] == '' or args[0] == '':
        return 'Address of cell is missing'
    first_int = get_int_from_expr(args[0], table)
    second_int = get_int_from_expr(args[1], table)
    if type(first_int) == int and type(second_int) == int:
        if operand == '+':
            result = first_int + second_int
        elif operand == '-':
            result = first_int - second_int
        elif operand == '*':
            result = first_int * second_int
        elif operand == '/':
            if second_int == 0:
                return 'Division by zero'
            else:
                result = int(first_int / second_int)
    else:
        return 'Incorrect cell address'
    return result

def data_checker(table):
    '''
    Проверка корректности ячеек таблицы
    '''
    err_message = ''
    for i in range(1, len(table)):
        for j in range(1, len(table[i])):
            try:
                table[i][j] = int(table[i][j])
            except:
                if table[i][j][0] != '=':
                    err_message = 'Missing = symbol before the expression in the cell '
                    err_message += table[0][j] + table[i][0]
                    return err_message
                expression = table[i][j][1:]
                expr_result = compute_expression(expression, table)
                if type(expr_result) == int:
                    table[i][j] = expr_result
                else:
                    return expr_result

if __name__ == "__main__":
    filename = sys.argv[1]
    table = csv_loader('test/'+filename)
    address_checker_message = address_checker(table)
    if address_checker_message:
        show_csv(table)
        sys.exit(address_checker_message)
    data_checker_message = data_checker(table)
    if data_checker_message:
        show_csv(table)
        sys.exit(data_checker_message)
    show_csv(table)