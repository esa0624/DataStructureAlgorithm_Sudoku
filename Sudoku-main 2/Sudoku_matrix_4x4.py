# didn't sure if we need a class or not
import random
import sys

import numpy as np

import dancing_link


def matrix_col_indices(row, col, num):
    """
    Use the indices of sudoku and value of each cell to get the index of col number of that binary matrix, we may use
    later on the exact-cover algorithm
    :param row: the row index of sudoku
    :param col: the col index of sudoku
    :param num: the number we fill in the cell of sudoku
    :return: a tuple of indices that refer to our 4 constraint
    """

    return [(row * 4 + col), (row * 4 + num + 15), (col * 4 + num + 31), ((row // 2 * 2 + col // 2) * 4 + num + 47)]


# for the sudoku initialization
def sudoku_init(initial_numbers):
    # dic is to store the (row,col,num)
    sudoku_dic = {}
    constraint = set()
    while len(sudoku_dic) < initial_numbers:
        # get random rows
        row = random.randint(0, 3)
        # get random columns
        col = random.randint(0, 3)
        fill_in_num = [1, 2, 3, 4]
        num = random.choice(fill_in_num)
        # check if (row, col) is already in the dic
        # if in, next round
        if (row, col) in sudoku_dic:
            continue
        # call the formula function to check if the constraint repeat or not
        col_indices = matrix_col_indices(row, col, num)
        has_repeat = False
        for i in col_indices:
            if i in constraint:
                has_repeat = True
        if has_repeat:
            continue
        else:
            constraint.update(col_indices)
            sudoku_dic[(row, col)] = num
    return sudoku_dic


def get_row_index(row, col, num):
    """
    Use the row, col index of sudoku and num we fill in the cells, we can get row index of matrix
    :param row:
    :param col:
    :param num:
    :return:
    """
    return (row * 4 + col) * 4 + num - 1


def generate_matrix(sudoku_dic):
    """
      We use this function to initialize matrix
      First, we sure that we have 324 cols:
           4*81 = 324
           Cause, we have 4 constraints:
           1. each cell of sudoku must have a number (a)
           2. each row of sudoku must not have the same number (b)
           3. each column of sudoku must not have the same number (c)
           4. each 3*3 grid must not have the same number (d)
           As we need to fill in 81 cells, we need to determine whether these 81 cells meet with these 4 constraints,
           that is to determine 4*81 YES/NO (1 or 0), so we need to raise a binary matrix with 324 cols. We determine our
           dancing linked list have 324 heads
       Then, we try to infer our rows number:
           We initialize our sudoku with 11 numbers and all the other 81-11 = 70 cells are empty. For each empty cell, we
           the maximum hypothesis as 9 possible numbers to fill in (1-9), than we have 70*90 = 630 possibilities. Also, we
           already have 11 numbers, which are fixed. So overall we will have 630 + 11 = 641 rows
       Thus, we have the binary matrix that is [641(rows) x 342(cols)]
       :param: row
       :param: col
       :param: num
       :return: sudoku_matrix
      """
    sudoku_matrix = dancing_link.DancingLinks(64, 64)
    for row in range(4):
        for col in range(4):
            # if the location already has the number
            if (row, col) in sudoku_dic:
                num = sudoku_dic[(row, col)]
                col_indices = matrix_col_indices(row, col, num)
                # we get the matrix's row index from the following formula
                row_index = get_row_index(row, col, num)
                # use the dancing link method append row
                sudoku_matrix.append_row(col_indices, row_index)
            # if the location do not have number yet
            else:
                # fill in with 1-9
                for num in range(1, 5):
                    col_indices = matrix_col_indices(row, col, num)
                    # we get the matrix's row index from the following formula
                    row_index = get_row_index(row, col, num)
                    # use the dancing link method append row
                    sudoku_matrix.append_row(col_indices, row_index)
    return sudoku_matrix


def print_init(dic):
    """
    This function is for testing, if I initialize the sudoku board and matrix right
    :param dic:
    :return:
    """
    rows = cols = 4
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    for (row, col), num in dic.items():
        board[row][col] = num
    for row in board:
        print(row)


init_numbers = 2
init_dic = sudoku_init(init_numbers)
print_init(init_dic)
matrix = generate_matrix(init_dic)
ans = []
dancing_link.DancingLinks.dancing(matrix, ans)
print(ans)
def print_answer(ans, init_dic):
    """
    This function is to print the full fill sudoku board, by the list of answers, that list include all the matrix's
    row index we raise up for the answer
    :param ans:
    :param init_dic:
    :return:
    """
    rows = cols = 4
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    for (row, col), num in init_dic.items():
        board[row][col] = num
    # from the row index of our answer list, we can use some formula to get the sudoku's row, col and num
    for row_index in ans:
        row = row_index//16
        col = (row_index % 16)//4
        num = (row_index % 16) % 4 + 1
        board[row][col] = num

    # print the full board
    for row in board:
        print(row)


print_answer(ans, init_dic)





'''
# following somehow is the debugging code used to view the output
write(matrix)
np.set_print_options(threshold=np.inf)
print(matrix.to_array())
file1 = open("matrix.txt", "w")
file1.write(str(matrix.to_array()))
'''
