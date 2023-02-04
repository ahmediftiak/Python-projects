import csv

class Board:
    def __init__(self, filename=None):
        if filename:
            self.load(filename)
    
    def load(self, filename):
        self.values = list(csv.reader(open(filename, 'r')))
        self.nrows = len(self.values)
        self.ncols = len(self.values[0])
    
    def save(self, filename):
        csv.writer(open(filename, 'w')).writerow(self.values)
    
    def print(self):
        print('\n'.join(map(''.join, map(lambda x: map(lambda y: f'{y:>3}', x), self.values))))
    
    def getLongestEqualSequence(self):
        offset = ((-1,-1), (-1,0), (-1, 1), (0,-1))
        longest = (-1,-1,-1,-1)
        F = [[[0,0,0,0] for j in range(self.ncols)] for i in range(self.nrows)]
        for i in range(self.nrows):
            for j in range(self.ncols):
                v = self.values[i][j]
                for d, o in enumerate(offset):
                    r, c, prev = i +o[0], j+o[1], 0
                    if (r>=0 and c>=0 and c<self.ncols and self.values[r][c]==v):
                        prev = F[r][c][d]
                    F[i][j][d] = prev+1
                    longest = max(longest, (prev+1, i, j, o))
        return longest

    def maskSequence(self, size, r, c, offset, val ='#'):
        for i in range(size):
            self.values[r][c] = val
            r += offset[0]
            c += offset[1]

board = Board()
for i in range(1,5):
    board.load(f'board{i}.csv')
    seq = board.getLongestEqualSequence()
    board.maskSequence(*seq)
    # board.print()
    # print()