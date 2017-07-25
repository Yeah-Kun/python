'''
	made by Ian in 2017-7-22 13:04:48
	井字棋，按照教程编写
'''
import random
import copy


def drawBoard(board):
    # 显示棋盘
    #print('  |  |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('------------')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('------------')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])


def inputPlayerLetter():
    # 玩家选择执 x 还是 o
    letter = None
    while not (letter == 'x' or letter == 'o'):
        letter = input("You want to be x or o : ").lower()

    if letter == 'x':
        return ['x', 'o']
    else:
        return ['o', 'x']


def whoGoesFirst():
    # 随机判断，谁先走
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # 如果想继续玩，就返回True，否则返回False
    print("Do you want to play again?(yes or no)")
    return input().lower().startswith('y')


def makeMove(board, letter, move):
    # 记录走的步，为什么不需要返回值？因为我们已经修改了引用
    board[move] = letter


def isWinner(bo, le):  # bo = board, le = letter
    # 判断玩家是否获胜,获胜返回True，否则返回False
    # 共有8种情况:|||三\/
    return (
        (bo[7] == le and bo[4] == le and bo[1] == le) or
        (bo[8] == le and bo[5] == le and bo[2] == le) or
        (bo[9] == le and bo[6] == le and bo[3] == le) or
        (bo[7] == le and bo[8] == le and bo[9] == le) or
        (bo[4] == le and bo[5] == le and bo[6] == le) or
        (bo[1] == le and bo[2] == le and bo[3] == le) or
        (bo[7] == le and bo[5] == le and bo[3] == le) or
        (bo[1] == le and bo[5] == le and bo[9] == le)
    )


def getBoardCopy(board):
    # 深拷贝棋盘列表
    dupeBoard = copy.deepcopy(board)
    return dupeBoard


def isSpaceFree(board, move):
    # 判断棋盘某个位置是否可走,可走返回True
    return (board[move] == ' ')


def getPlayMove(board):
    # 玩家落子
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
    	move = input("What is your next move?(1-9):")
    return int(move)


def chooseRandomMoveFromList(board, moveList):
    # 从可以落子列表里选择一个落子，用于电脑AI
    possibleMoves = []
    for i in moveList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


def getComputerMove(board, computerLetter):
    # 计算机AI
    if computerLetter == 'x':
        playerLetter = 'o'
    else:
        playerLetter = 'x'

    # AI判断自己是否落子即胜，模拟下棋，遍历所有结果
    for i in range(1, 10):
        copyBoard = getBoardCopy(board)
        if isSpaceFree(copyBoard, i):
            makeMove(copyBoard, computerLetter, i)
            if isWinner(copyBoard, computerLetter):
                return i

    # AI判断玩家是否落子即胜
    for i in range(1, 10):
        copyBoard = getBoardCopy(board)
        if isSpaceFree(copyBoard, i):
            makeMove(copyBoard, playerLetter, i)
            if isWinner(copyBoard, playerLetter):
                return i

    # 先下角，再下中间，最后下边
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move
    if isSpaceFree(board, 5):
        return 5
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isBoardFull(board):
    # 判断棋盘是否已满
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

if __name__ == '__main__':
    print("====Tic Tac Toe====")
    while True:
        theBoard = [' '] * 10  # 初始化棋盘列表
        playerLetter, computerLetter = inputPlayerLetter()  # 决定执什么棋，谁先走
        turn = whoGoesFirst()
        print("The " + turn + " will go first.")
        gameIsPlaying = True
        while gameIsPlaying:
            if turn == 'player':
            	# 玩家
                drawBoard(theBoard)
                move = getPlayMove(theBoard)
                makeMove(theBoard, playerLetter, move)

                if isWinner(theBoard, playerLetter):
                	# 判断玩家是否赢了
                    drawBoard(theBoard)
                    print('Hooray! You have won the game!')
                    gameIsPlaying = False

                else:
                    if isBoardFull(theBoard):
                    # 判断棋盘是否已满
                        drawBoard(theBoard)
                        print("The game is a tie.")
                        break

                    else:
                        turn = 'computer'

            else:
            	# 电脑
                move = getComputerMove(theBoard, computerLetter)
                print(theBoard)
                makeMove(theBoard, computerLetter, move)

                if isWinner(theBoard, computerLetter):
                    drawBoard(theBoard)
                    print('The computer win')
                    gameIsPlaying = False

                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print("The game is a tie.")
                        break

                    else:
                        turn = 'player'

        if not playAgain():
            break
