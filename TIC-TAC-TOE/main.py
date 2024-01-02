from Game import Game
def main():
    game=Game()
    print("HOW TO PLAY: ")
    print("-You will play as 'O', AI will play as 'X'.")
    print("-You will play first.")
    print("-Select a valid cell to play your mark in.")
    print("-To select a cell, use Row and Column")
    print("-eg.\n00|01|02")
    print("--------")
    print("10|11|12")
    print("--------")
    print("20|21|22")
    print("to selct `12` cell, Row=1 Column=2")
    turn="Player"
    while(not game.gameEndCheck()):
        game.boardCurrState.printBoard()
        if(turn=="Player"):
            print("Play your move:")
            row=int(input("Row: "))
            col=int(input("Col: "))
            print(" ")
            game.playerTurn(row, col)
            turn="AI"
        else:
            if(game.gameEndCheck()):
                break
            game.AITurn()
            turn="Player"
    game.boardCurrState.printBoard()
    print("Game ended")

main()