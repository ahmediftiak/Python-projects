import sys
import csv

with open(sys.argv[1], 'r') as file:
    reader = csv.reader(file)
    board = list(reader)
    row = len(board)
    com = len(board[0])

current_line  = []
longest_line = []
   
for i in range(row):
    for j in range(com):
        
        if i < row-1 and board[i][j] == board[i+1][j]:# top down
            current_line.append((i,j))
            for k in range(i, row-1):                
                if board[k][j] == board[k+1][j]:
                    current_line.append((k+1,j))
                else:
                    break

            if len(current_line) > len(longest_line):
                longest_line = current_line
            current_line = []
            
        
        if j < com-1 and board[i][j] == board[i][j+1]:# left to right
            current_line.append((i,j))
            for k in range(j, com-1):                
                if board[i][k] == board[i][k+1]:
                    current_line.append((i,k+1))
                else:
                    break
            
            if len(current_line) > len(longest_line):
                longest_line = current_line
            current_line = []    

        if i < row-1 and j < com-1 and board[i][j] == board[i+1][j+1]:# diagonal 
            v = j
            current_line.append((i,j))
            for k in range(i, row-1):
                if board[k][v] == board[k+1][v+1]:
                    current_line.append((k+1,v+1))
                else: 
                    break
                if v < com-2:
                    v += 1

            if len(current_line) > len(longest_line):
                longest_line = current_line
            current_line = []            
      
        if i < row - 1 and j != 0 and board[i][j] == board[i+1][j-1]:# anti diagonal
            w = i 
            current_line.append((i,j))
            for k in range(j, 0, -1):
                if board[w][k] == board[w+1][k-1]:
                    current_line.append((w+1, k-1))
                else:
                    break
                if w < row-2:
                    w += 1

            if len(current_line) > len(longest_line):
                longest_line = current_line
            current_line = []

#print(longest_line)