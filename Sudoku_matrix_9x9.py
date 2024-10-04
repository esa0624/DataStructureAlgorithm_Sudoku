# didn't sure if we need a class or not
import random
import sys

import numpy as np

import dancing_link


def matrix_col_indices(row, col, num):
    """
    Use the indices of sudoku and value of each cell to get the index of col number of that binary matrix, we may use
    later on the exact-cover algorithm.
    These formulas stand for positioning to columns in binary matrix corresponding the row, cols and num on sudoku board.
    The first formula is (row * 9 + col),which is in bound of 81 cols(0-80) in matrix. As we have 81 cells in sudoku,
    81 0/1(s), means to whether these 81 cells have number or not.
    The second formula is (row * 9 + num + 80), which is in bound of 81-161, plus 80 means that we start from 81 col in
    matrix. When we fill in the sudoku, we need to think whether each row have 1-9, that part will
    be row*9 + num.
    The third formula is (col * 9 + num + 161), which is in bound of 162-242, plus 161 means we start from 161 cols, that
    is the third part of constraints. We need to determine whether each col have 1-9, which the
    mathematical expression is col*9 + num.
    The fourth formula is (row // 3 * 3 + col // 3) * 9 + num + 242, that the bound is 243-323, plus 242 means we start
    from 242 cols, the fourth part of constraints. row//3 x 3 + col//3 calculates which of the nine blocks (numbered 0-8) the
    current cell belongs to. row//3 will have the result 0 or 1 or 2 which will locate to the up 3 rows, middle 3 rows and bottom
    3 rows, then we multiple 3, will have (0, 3, 6) which is the start row number of each block. Plus col//3 means the left 3 cols
    middle 3 cols and right 3 cols. Multiple 9 by row // 3 * 3 + col // 3 is because we have 9 possible number 1-9 to fill in, as
    what we do for the previous two. Plus number we fill in and the displace number 242.
    and then multiplies it by 9 and plus num means determine whether each block have 1-9 and
    appear once.
    :param row: the row index of sudoku
    :param col: the col index of sudoku
    :param num: the number we fill in the cell of sudoku
    :return: a tuple of indices that refer to our 4 constraint
    """

    return [(row * 9 + col), (row * 9 + num + 80), (col * 9 + num + 161), ((row // 3 * 3 + col // 3) * 9 + num + 242)]


# for the sudoku initialization
def sudoku_init(initial_numbers):
    """
    This function is to initialize the sudoku board. Our way is to guarantee that the first 9 number we fill in will not
    fill in the same row, col or block, which will reduce the likelihood that the generated sudoku has no solution. We
    also use our four constraints to avoid repeat and conflicts when we initialize the sudoku.
    :param initial_numbers: how many number we want the sudoku problem to have when we initialize them
    :return: sudoku_dic: Dictionary containing the numeric coordinates and numbers we've filled in during initialization
    """
    sudoku_dic = {}
    constraint = set()

    while len(sudoku_dic) < initial_numbers:
        blocks = list(range(9))
        rows = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        cols = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        nums = list(range(1, 10))
        for _ in range(9):
            block = blocks.pop(random.randint(0, len(blocks) - 1))
            row = rows[block // 3].pop(random.randint(0, len(rows[block // 3]) - 1))
            col = cols[block % 3].pop(random.randint(0, len(cols[block % 3]) - 1))
            num = nums.pop(random.randint(0, len(nums) - 1))
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
                if len(sudoku_dic) == initial_numbers:
                    return sudoku_dic
    return sudoku_dic

def sudoku_init_rand(initial_numbers):
    # dic is to store the (row,col,num)
    sudoku_dic = {}
    constraint = set()
    while len(sudoku_dic) < initial_numbers:
        # get random rows
        row = random.randint(0, 8)
        # get random columns
        col = random.randint(0, 8)
        fill_in_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
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
    Use the row, col index of sudoku and num we fill in the cells, we can get row index of matrix. The idea is row * 9 +
    col part can locate to the cell of that 81. *9 means that each cell can be fill with 9 possible number. num-1 is to
    convert the filled in numbers 1 through 9 to 0 through 8, since we are counting from 0.
    :param row: The row of cell in sudoku
    :param col: The col of cell in sudoku
    :param num: The num of cell in sudoku
    :return:
    """
    return (row * 9 + col) * 9 + num - 1


def generate_matrix(sudoku_dic):
    """
      We use this function to initialize matrix
      First, we sure that we have 324 cols:
           4*81 = 324
           Cause, we have 4 constraints (as we talked before in matrix_col_indices):
           1. each cell of sudoku must have a number
           2. each row of sudoku must not have the same number
           3. each column of sudoku must not have the same number
           4. each 3*3 grid must not have the same number
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
    sudoku_matrix = dancing_link.DancingLinks(729, 324)
    for row in range(9):
        for col in range(9):
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
                for num in range(1, 10):
                    col_indices = matrix_col_indices(row, col, num)
                    # we get the matrix's row index from the following formula
                    row_index = get_row_index(row, col, num)
                    # use the dancing link method append row
                    sudoku_matrix.append_row(col_indices, row_index)
    return sudoku_matrix


def print_init(dic):
    """
    This function is for testing, if I initialize the sudoku board and matrix right
    :param dic: Print the dictionary with initialize (row, col) as indices and nums as value.
    :return:
    """
    rows = cols = 9
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    for (row, col), num in dic.items():
        board[row][col] = num
    for row in board:
        print(row)



def get_completed_sudoku(init_dic):
    """
    This function is raised a calling dancing link function to get answer from the sudoku dictionary we initialize with
    initial numbers
    :param init_dic:
    :return: ans
    """
    matrix = generate_matrix(init_dic)
    ans = []
    matrix.dancing(ans)
    return ans[0]

def check_unique_answer(init_dic):
    """
    This function is raised to check, if we dig inside a full sudoku, can we guarantee that we only have a unique answer.
    :param init_dic:
    :return: whether we only have one solution for that sudoku or not
    """
    matrix = generate_matrix(init_dic)
    ans = []
    matrix.dancing(ans, 2, [])
    '''for i in ans:
        print(answer_to_sudoku(i))'''
    return len(ans) == 1

def generate_sudoku_problems(sudoku, counter):
    """
    This function is raised to generate the sudoku problems, we will randomly make one cell empty each time and calling
    dancing link to solve the problem, and check if the sudoku problem have unique answer.
    If that sudoku problem do not have unique answer, backtrack
    :param sudoku:
    :param counter:
    :return:
    """
    print(counter)
    if counter == 0:
        return True
    sudoku_dic = to_dic(sudoku)
    keys = list(sudoku_dic.keys()).copy()

    while len(keys) > 0:
        # randomly choose key from the sudoku list
        choice_cell = keys.pop(random.randint(0, len(keys)-1))

        # need to store the original value in a variable
        original = sudoku_dic.pop(choice_cell)
        if check_unique_answer(sudoku_dic):
            counter = counter - 1
            sudoku[choice_cell[0], choice_cell[1]] = 0
            print(sudoku)
            if generate_sudoku_problems(sudoku, counter):
                return True
        else:
            # recover the original, and do not change the counter
            sudoku_dic[choice_cell] = original


def to_dic(sudoku: np.ndarray):
    """
    This function is raised to convert sudoku to dict form
    :param sudoku: sudoku (np.ndarray): 9*9 NDArray representing an uncompleted (or completed) sudoku
    :return: dict: dict of numbers in sudoku with (row, col) tuple as a key and number at that position as a value.
    """
    sudoku_dic = {}
    for r in range(sudoku.shape[0]):
        for c in range(sudoku.shape[1]):
            if sudoku[r, c] != 0:
                sudoku_dic[(r, c)] = sudoku[r, c]
    return sudoku_dic


def answer_to_sudoku(ans):
    """
    This function is using the following formula to convert the row indices from the binary matrix to the coordinate and
    num on sudoku, which is the inverse process of this equation(row * 9 + col) * 9 + num - 1.
    :param ans: The list of row index from the binary matrix of the answer of sudoku
    :return: board
    """
    board = np.zeros((9, 9), int)

    # from the row index of our answer list, we can use some formula to get the sudoku's row, col and num
    for row_index in ans:
        row = row_index//9//9
        col = row_index//9 % 9
        num = row_index % 9 + 1
        board[row, col] = num

    # print the full board
    return board



"""
Following are some local test we use 
"""

"""init_numbers = 0
init_dic = sudoku_init(init_numbers)
ans = get_completed_sudoku(init_dic)
completed_sudoku = answer_to_sudoku(ans)
print(completed_sudoku)


#generate_sudoku_problems(completed_sudoku, counter=56)
#print(completed_sudoku)"""


'''

# following somehow is the debugging code used to view the output
write(matrix)
np.set_print_options(threshold=np.inf)
print(matrix.to_array())
file1 = open("matrix.txt", "w")
file1.write(str(matrix.to_array()))
'''

"""
sudoku = np.array([
  [0, 9, 0, 0, 0, 8, 0, 4, 5]
, [1, 0, 0, 0, 0, 9, 6, 0, 0]
, [3, 5, 0, 2, 0, 0, 0, 0, 0]
, [8, 0, 0, 5, 0, 3, 0, 0, 0]
, [0, 0, 2, 0, 0, 7, 0, 0, 0]
, [0, 0, 0, 0, 8, 0, 0, 0, 0]
, [4, 0, 0, 0, 0, 0, 0, 3, 2]
, [5, 0, 0, 9, 0, 1, 0, 0, 8]
, [9, 8, 0, 0, 0, 0, 0, 0, 0]
])
dic = to_dic(sudoku)
#ans = get_completed_sudoku(dic)
print(check_unique_answer(dic))
"""
