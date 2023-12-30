class Board:
    def __init__(self):#calling default cunstructor
        self.rows=3
        self.cols=3
        self.board=[[" " for i in range(self.cols)] for j in range(self.rows)]
    def printBoard(self):
        for i in range(5):
            if(i%2==0):
                for j in range(5):
                    if(j%2 == 0):
                        print(self.board[int(i/2)][int(j/2)], end='')
                    else:
                        print("|", end='')
            else:
                print("\n_____")
        print("\n")
    
    def emptyPositions(self):
        emptyPos=[(i,j) for i in range(3) for j in range(3) if self.board[i][j]==" "]
        return emptyPos