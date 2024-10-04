# Team TEA: Sudoku
## Introduction
As all of our members are interested in solving sudoku, our project is to explore the data structure and algorithm behind sudoku by solving the problem of generating a random 9*9 sudoku with exactly one unique solution and providing a User Interface to try the sudoku puzzle we generate. In addition, we compared the two algorithms for generating and solving sudoku: Dancing Link with Algorithm X (DLX) and Depth First Search (DFS), and the comparison between their performance is shown by plots. 

The process to achieve our goal is to first convert the sudoku problem to the Exact Cover problem and use Knuth's Algorithm X to find the solution to the Exact Cover problem. We can then solve the sudoku problem by that solution. To implement Knuth's Algorithm X, we implement the data structure, Dancing Links, from scratch instead of using 2D arrays to improve the runtime and performance. This project covers learning data structures and algorithms, which aligns with our expectation to learn some complex data structures and algorithms that might not be covered in class. 


## Instruction
### Performance Comparison
1. Download the whole repository.
2. Open the repository with Jupyter Lab.
3. Run the `test.ipynb` file in your Jupyter Lab by pressing `Shift + Enter`.
4. The plots will be generated and displayed.
5. Look at the plot and compare the runtime of DLX and DFS.

To test the performance, we try two different ways to initialize the fixed numbers: Random and Non-repeat. The first way is the random picking, which is to randomly fill out some cells by randomly picking N fixed numbers. After that, we randomly fill out other cells while keep checking if putting that number into a specific position will still comply with the sudoku rule, which is that each row, each column, and each block all has numbers 1 ~ 9 without any duplicates. The second way is the non-repeat choosing, which is to randomly choose N fixed numbers but making sure that the first 9 numbers of N fixed numbers we pick are all in different row, column, and block. Then, we randomly pick positions for the remaining (N-9) numbers. The purpose for this is to reduce the runtime it may take by avoiding too much overlapping in rows, columns, and blocks, which will increase the difficulty to fill out other cells and make the runtime longer.

The following is the comparison study of performance of DLX and DFS for which we ran initial numbers from 0 to 20 and texted each 2000 trials:
![Plots](/../main/images/comparison.jpg)

### Sudoku UI
1. Download the whole repository.
2. Open your Terminal.
3. Go to the downloaded repository and go to the folder where the `sudoku.py` file locates.
4. Run the `sudoku.py file` by the command `python sudoku.py`
5. A window will show up with a solvable sudoku puzzle.
6. Click on the empty cell in the sudoku puzzle and input a number to it by keyboard.
7. To replace the existing number you inputted, just click on it again and input a number by keyboard.
8. Once finishing inputting all the empty cells, click on the `“Check” button` on the left to check if your solution is correct.
9. The window will show a small message below the `“Clear” button` informing your results of whether you solve the puzzle
   - If you succeed, you can click on the `“New” button` to start a new game.
   - If you fail, you can either click on the `“New” button` to start a new game or click on the `“Clear” button` to restart and retry the same game.
10. Finally, close the window to quit the game.

The following is the screenshot of the UI we provided:
![Sudoku UI Screenshot](/../main/images/sudoku_ui_screenshot.png)
