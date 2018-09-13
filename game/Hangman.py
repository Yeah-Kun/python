'''
	made by YeahKun in 2017-7-21 15:11:02
	猜字谜游戏，可重复开始游戏
	事先预设好单词，玩家猜单词中的字母，猜对继续，猜错则画火柴人一部分
	当猜对单词所有字母，玩家获胜，当火柴人画完，玩家失败
'''
import random

HANGMANPICS = [
'''
=====
+---+
|   |
	|
	|
	|
	|
=====''',
'''
=====
+---+
|   |
O	|
	|
	|
	|
=====''',
'''
=====
+---+
|   |
O	|
|	|
	|
	|
=====''',
'''
======
 +---+
 |   |
 O	 |
/|	 |
	 |
	 |
======''',
'''
======
 +---+
 |   |
 O	 |
/|\	 |
	 |
	 |
======''',
'''
======
 +---+
 |   |
 O	 |
/|\	 |
/	 |
	 |
======''',
'''
======
 +---+
 |   |
 O	 |
/|\	 |
/ \	 |
	 |
======'''
]

# 囊括所有神秘单词的长字符串
words = '''Industries that are expected to play leading role in the AI will be fully bolstered by strengthening technology transformation, 
especially in areas such as the internet of things, intelligent hardware and software, 
as well as smart robots. Industrial upgrading in areas such as smart manufacturing, 
connected farming as well as home automation (smart home) will be encouraged. 
It was singled out in the guideline China aim for an AI industry worth of over 150 billion yuan by 2020.'''.split()


def getRandomWord(wordList):
    # 获取单词长度，然后随机返回单词的某个字母
    letter = random.randint(0, len(wordList) - 1)
    return wordList[letter]


def disPlayGround(HANGMANPICS, missedLetters, correctLetters, serectWord):
        # 游戏显示板，用于展现游戏情况
    print(HANGMANPICS[len(missedLetters)], end='\n')
    print('Missed letters:', end='')
    for letter in missedLetters:
        print(letter, end=' ')
    print()  # 起到换行的作用，为了美观好看

    blanks = '_' * len(serectWord)

    for i in range(len(serectWord)):
        # 用猜对的单词替代空白位置
        if serectWord[i] in correctLetters:
            blanks = blanks[:i] + serectWord[i] + blanks[i + 1:]

    for letter in blanks:
        # 展示神秘单词的全部内容
        print(letter, end=' ')


def getGuess(alreadyGuessed):
        # 确保玩家只输入一个字母
    while True:
        print('\nGuess a letter:')
        guess = input()
        if len(guess) != 1:
            print("Please enter a single letter.")
        elif guess in alreadyGuessed:
            print("You have already guessed that letter,Choose again.")
        elif guess.isalpha() == False:
            print("Please enter a letter.")
        else:
            return guess


def playAgain():
    # 如果玩家想继续玩，返回True，否则返回False
    print('Do you want to play again?(yes or no)')
    return input().lower().startswith('y')


if __name__ == '__main__':
    print('H A N G M A N')
    missedLetters = ''  # 玩家已经猜过的不属于神秘单词的字符串
    correctLetters = ''  # 玩家已经猜过的属于神秘单词的字符串
    serectWord = getRandomWord(words)  # 获得随机的神秘单词
    gameIsDone = False

    while True:
        disPlayGround(HANGMANPICS, missedLetters,
                      correctLetters, serectWord)  # 显示游戏版

        # 玩家输入猜测字母
        guess = getGuess(missedLetters + correctLetters)  # 玩家输入过的字母构成的字符串

        # 判断字母是否属于神秘单词中
        if guess in serectWord:  # 如果属于
            correctLetters = correctLetters + guess

            # 判断玩家是否获胜
            foundAllLetters = True
            for i in range(len(serectWord)):
                if serectWord[i] not in correctLetters:
                    foundAllLetters = False
                    break

            if foundAllLetters:
                print("Yes! The secret word is " +
                      serectWord + "! You have won!")
                gameIsDone = True

        else:
            missedLetters = missedLetters + guess

            #
            if len(missedLetters) == len(HANGMANPICS) - 1:
                disPlayGround(HANGMANPICS, missedLetters,
                              correctLetters, serectWord)
                print("\nYou have run out of guesses!\n " + "The secret word is " + serectWord + "\nAfter " + str(len(missedLetters)) + " missed guesses and " +
                      str(len(correctLetters)) + " correct guesses, the word was" + serectWord)
                gameIsDone = True

        if gameIsDone:
            if playAgain():
                missedLetters = ''
                correctLetters = ''
                gameIsDone = False
                serectWord = getRandomWord(words)

            else:
                break
