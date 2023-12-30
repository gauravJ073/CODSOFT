from Board import Board

#exception for handling invalid moves
class InvalidMove(Exception):
    pass

class Game:
    #creating a constructor to initialize game variables
    def __init__(self): 
        self.boardCurrState=Board()
        self.AIMark="X"
        self.playerMark="O"
    
    
    
    #funciton to mark a move made by any player
    def __makeMove(self, boardState , player, row, col):
        try:#using exception handling to make sure error doesnt occurs
            if (((player=="O") or (player=="X")) and (boardState.board[row][col]==" ")):
                boardState.board[row][col]=player
                return True
            else:
                raise InvalidMove("Invalid move played")
        except InvalidMove:
            print("only 'X' and 'O' are valid moves on empty cells")
            return False
            

    #function to check if specified player has won the game
    def checkWinner(self, boardState, player):
        for row in boardState.board:
            if all(cell == player for cell in row):
                return True

        for col in range(3):
                if all(boardState.board[row][col] == player for row in range(3)):
                    return True

        if all(boardState.board[i][i] == player for i in range(3)) or all(boardState.board[i][2 - i] == player for i in range(3)):
            return True

        return False

    def __minmax(self, boardState, currPlayer):#minmax to evaluate score of a move
        #getting all possible moves using empty positions
        possibleMoves=boardState.emptyPositions()
        
        #checking if any plyer has won or if there is no possible moves left
        if (self.checkWinner(boardState, self.playerMark)):
            return -1
        if (self.checkWinner(boardState, self.AIMark)):
            return 1
        if (possibleMoves==[]):
            return 1
        
        #using recursion to go through each possible move and get the maximum score for AI and minimum for Human player
        #sum the scores of each
        #choose best score
        if currPlayer==self.AIMark:
            max_score=float("-inf")
            score=0
            for move in possibleMoves:
                self.__makeMove(boardState, self.AIMark, move[0], move[1])
                score+=self.__minmax(boardState, self.playerMark)
                boardState.board[move[0]][move[1]]=" "
                max_score=max(max_score, score)
            return max_score
        
        else:
            min_score=float("inf")
            score=0
            for move in possibleMoves:
                self.__makeMove(boardState, self.playerMark, move[0], move[1])
                score+=self.__minmax(boardState, self.AIMark)
                boardState.board[move[0]][move[1]]=" "
                min_score=min(min_score, score)
            return min_score

    #function to get the best move for AI player
    def __bestMove(self, boardState):
        max_score=float("-inf")
        bestmove=None
        possibleMoves=boardState.emptyPositions()

        
        for move in possibleMoves:
            self.__makeMove(boardState, self.AIMark, move[0], move[1])
            if(self.checkWinner(boardState, self.AIMark)):
                boardState.board[move[0]][move[1]]=" "
                return move
            
            move_score=self.__minmax(boardState, self.playerMark)
            boardState.board[move[0]][move[1]]=" "
            
            if move_score>max_score:
                max_score=move_score
                bestmove=move
        
        
        return bestmove

    def gameEndCheck(self):
        if (self.checkWinner(self.boardCurrState, self.playerMark)):
            print("Human won")
            return True
        if (self.checkWinner(self.boardCurrState, self.AIMark)):
            print("AI won")
            return True
        if (self.boardCurrState.emptyPositions==[]):
            print("No one won")
            return True
        return False
    #function to make move for AI
    def AITurn(self):
        move=self.__bestMove(self.boardCurrState)
        if(self.__makeMove(self.boardCurrState, self.AIMark, move[0], move[1])):
            return True
        else:
            return False

    #funciton to make move for Human player
    def playerTurn(self, row, col):
        if(self.__makeMove(self.boardCurrState, self.playerMark, row, col)):
            return True
        else:
            return False

