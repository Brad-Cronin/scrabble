NUM_ROWS_COLS = 15


def scrabbleBoard():
    board = [["TW", 0, 0, "DL", 0, 0, 0, "TW", 0, 0, 0, "DL", 0, 0, "TW"],
             [0, "DW", 0, 0, 0, "TL", 0, 0, 0, "TL", 0, 0, 0, "DW", 0],
             [0, 0, "DW", 0, 0, 0, "DL", 0, "DL", 0, 0, 0, "DW", 0, 0],
             ["DL", 0, 0, "DW", 0, 0, 0, "DL", 0, 0, 0, "DW", 0, 0, "DL"],
             [0, 0, 0, 0, "DW", 0, 0, 0, 0, 0, "DW", 0, 0, 0, 0],
             [0, "TL", 0, 0, 0, "TL", 0, 0, 0, "TL", 0, 0, 0, "TL", 0],
             [0, 0, "DL", 0, 0, 0, "DL", 0, "DL", 0, 0, 0, "DL", 0, 0],
             ["TW", 0, 0, "DL", 0, 0, 0, "DW", 0, 0, 0, "DL", 0, 0, "TW"],
             [0, 0, "DL", 0, 0, 0, "DL", 0, "DL", 0, 0, 0, "DL", 0, 0],
             [0, "TL", 0, 0, 0, "TL", 0, 0, 0, "TL", 0, 0, 0, "TL", 0],
             [0, 0, 0, 0, "DW", 0, 0, 0, 0, 0, "DW", 0, 0, 0, 0],
             ["DL", 0, 0, "DW", 0, 0, 0, "DL", 0, 0, 0, "DW", 0, 0, "DL"],
             [0, 0, "DW", 0, 0, 0, "DL", 0, "DL", 0, 0, 0, "DW", 0, 0],
             [0, "DW", 0, 0, 0, "TL", 0, 0, 0, "TL", 0, 0, 0, "DW", 0],
             ["TW", 0, 0, "DL", 0, 0, 0, "TW", 0, 0, 0, "DL", 0, 0, "TW"]]
    return board


def blankBoard():
    board = []
    for i in range(NUM_ROWS_COLS):
        board.append([])
        for j in range(NUM_ROWS_COLS):
            board[i].append(' ')
    return board


def scrabbleLetters():
    letters = {"A": 1}
    letters["B"] = 3
    letters["C"] = 3
    letters["D"] = 2
    letters["E"] = 1
    letters["F"] = 4
    letters["G"] = 2
    letters["H"] = 4
    letters["I"] = 1
    letters["J"] = 8
    letters["K"] = 5
    letters["L"] = 1
    letters["M"] = 3
    letters["N"] = 1
    letters["O"] = 1
    letters["P"] = 3
    letters["Q"] = 10
    letters["R"] = 1
    letters["S"] = 1
    letters["T"] = 1
    letters["U"] = 1
    letters["V"] = 4
    letters["W"] = 4
    letters["X"] = 8
    letters["Y"] = 4
    letters["Z"] = 10
    letters["*"] = 0
    return letters


def wordList():
    words = []
    f = open("scrabble_word_list.txt", "r")
    for i in f:
        word = i.strip()
        words.append(word)
    f.close()
    return words


def wordValue(word):
    letters = scrabbleLetters()
    value = 0
    dw = 0
    tw = 0
    for letter in word:
        if letter[1] == "DW":
            dw = dw + 1
            value = value + letters[letter[0]]
        elif letter[1] == "TW":
            tw = tw + 1
            value = value + letters[letter[0]]
        elif letter[1] == "DL":
            value = value + 2 * letters[letter[0]]
        elif letter[1] == "TL":
            value = value + 3 * letters[letter[0]]
        else:
            value = value + letters[letter[0]]
    return value * (2 ** dw) * (3 ** tw)


def gameState(opponent):
    with open(f'{opponent}_game.txt', 'r') as game:
        board = []
        for line in game:
            board.append(line.split(','))
    for row in board:
        row.remove('\n')
    return board


def rowColLetters(board, direction, start):
    dirVec = {'H': 0, 'V': 0}
    dirVec[direction] = 1
    letters = []
    for i in range(NUM_ROWS_COLS):
        letter = board[start * dirVec['H'] + i * dirVec['V']][start * dirVec['V'] + i * dirVec['H']]
        if letter != ' ':
            letters.append(letter)
    return letters


def turnScore(mainWord, playedLetters, direction, start, currentBoard):
    board = scrabbleBoard()
    wordlist = wordList()
    turnWords = []
    word = []
    dirs = [-1, 1]
    dirVec = {'H': 0, 'V': 0}
    dirVec[direction] = 1
    for i in range(len(mainWord)):
        bonusWord = []
        if mainWord[i] == playedLetters[i]:
            word.append((mainWord[i], board[start[0] + i * dirVec['V']][start[1] + i * dirVec['H']]))
            for j in dirs:
                n = 1
                while True:
                    row = start[0] + i * dirVec['V'] + n * j * dirVec['H']
                    col = start[1] + i * dirVec['H'] + n * j * dirVec['V']
                    if 0 <= row < NUM_ROWS_COLS:
                        if 0 <= col < NUM_ROWS_COLS:
                            bonusLetter = currentBoard[row][col]
                        else:
                            break
                    else:
                        break
                    if bonusLetter == ' ':
                        break
                    else:
                        bonusWord.append((bonusLetter, 0))
                        n += 1
            if len(bonusWord) > 0:
                bonusWord.append((mainWord[i], board[start[0] + i * dirVec['V']][start[1] + i * dirVec['H']]))
                l = len(bonusWord)
                bword = ''
                for k in range(l - n - 1, -1, -1):
                    bword = bword + bonusWord[k][0]
                bword = bword + bonusWord[-1][0]
                for k in range(l - n, l - 1):
                    bword = bword + bonusWord[k][0]
                if bword not in wordlist:
                    return 0
                turnWords.append(bonusWord)
        else:
            word.append((mainWord[i], 0))
    turnWords.append(word)
    score = 0
    for word in turnWords:
        score += wordValue(word)
    n = 0
    for letter in playedLetters:
        if letter != '?':
            n += 1
    if n == 7:
        score += 50
    return score


def bestMove(opponent, letters):
    board = gameState(opponent)
    myLetters = list(letters.upper())
    bestScore = 0
    bestWord = ''
    # Go twice through the board, once horizontal, once vertical
    for direction in ['H', 'V']:
        dirVec = {'H': 0, 'V': 0}
        dirVec[direction] = 1
        # For each direction, need to check every row/col
        for i in range(NUM_ROWS_COLS):
            # For each row/col, the available letters are from the existing
            # on the board in that row/col, plus myLetters
            print(f'{direction} - {i}')
            allLetters = myLetters + rowColLetters(board, direction, i)
            words = inMyLetters(str(allLetters))
            for word in words:
                # Possible positions to play the word (based on word length)
                for j in range(NUM_ROWS_COLS - len(word) + 1):
                    if not wordFitsOnBoard(board, word, direction,
                                           (i * dirVec['H'] + j * dirVec['V'], i * dirVec['V'] + j * dirVec['H'])):
                        continue
                    playedWord = ''
                    validWord = True
                    copyLetters = myLetters.copy()
                    # Go through each letter in the word
                    for k in range(len(word)):
                        # 'spot' is what's currently on the board in that location
                        spot = board[i * dirVec['H'] + (j + k) * dirVec['V']][i * dirVec['V'] + (j + k) * dirVec['H']]
                        # If the spot on the board is the letter in the word, then it's valid, but not a played letter
                        # If it's empty, see if you can add that as a played letter
                        # If neither, it's not a valid word
                        if spot == word[k]:
                            playedWord = playedWord + '?'
                        elif spot == ' ':
                            if word[k] in copyLetters:
                                playedWord = playedWord + word[k]
                                copyLetters.remove(word[k])
                            elif '*' in copyLetters:
                                playedWord = playedWord + word[k]
                                copyLetters.remove('*')
                            else:
                                validWord = False
                                break
                        else:
                            validWord = False
                            break
                    if validWord:
                        start = (i * dirVec['H'] + j * dirVec['V'], i * dirVec['V'] + j * dirVec['H'])
                        wordScore = turnScore(word, playedWord, direction, start, board)
                        if wordScore > bestScore:
                            bestScore = wordScore
                            bestWord = [word, direction, start, bestScore]
    return bestWord


# def bestMove2(opponent, letters):
#     board = gameState(opponent)
#     myLetters = list(letters.upper())
#     bestScore = 0
#     bestWord = ''
#     # Go twice through the board, once horizontal, once vertical
#     for direction in ['H', 'V']:
#         dirVec = {'H': 0, 'V': 0}
#         dirVec[direction] = 1
#         # For each direction, need to check every row/col
#         for i in range(NUM_ROWS_COLS):
#             # For each row/col, the available letters are from the existing
#             # on the board in that row/col, plus myLetters
#             print(f'{direction} - {i}')
#             if validWord:
#                 start = (i * dirVec['H'] + j * dirVec['V'], i * dirVec['V'] + j * dirVec['H'])
#                 wordScore = turnScore(word, playedWord, direction, start, board)
#                 if wordScore > bestScore:
#                     bestScore = wordScore
#                     bestWord = [word, direction, start, bestScore]
#     return bestWord


def wordFitsOnBoard(board, word, direction, start):
    dirVec = {'H': 0, 'V': 0, direction: 1}
    spot = (start[0] - dirVec['V'], start[1] - dirVec['H'])
    if spot[0] >= 0:
        if spot[1] >= 0:
            if board[spot[0]][spot[1]] != ' ':
                return False
    spot = (start[0] + (len(word) * dirVec['V']), start[1] + (len(word) * dirVec['H']))
    if spot[0] < NUM_ROWS_COLS:
        if spot[1] < NUM_ROWS_COLS:
            if board[spot[0]][spot[1]] != ' ':
                return False
    for i in range(len(word)):
        spot = board[start[0] + i * dirVec['V']][start[1] + i * dirVec['H']]
        if spot != ' ':
            if spot != word[i]:
                return False
        for j in [-1, 1]:
            spot = (start[0] + j * dirVec['H'] + i * dirVec['V'], start[1] + j * dirVec['V'] + i * dirVec['H'])
            onBoard = True
            for k in range(len(spot)):
                if spot[k] < 0:
                    onBoard = False
                    break
                elif spot[k] >= NUM_ROWS_COLS:
                    onBoard = False
                    break
            if onBoard:
                if board[spot[0]][spot[1]] != ' ':
                    return True
    return False


def makeMove(opponent, word, direction, start):
    board = gameState(opponent)
    for i in range(len(word)):
        if direction.upper() == 'H':
            board[start[0]][start[1] + i] = word[i].upper()
        else:
            board[start[0] + i][start[1]] = word[i].upper()
    with open(f'{opponent}_game.txt', 'w') as game:
        for line in board:
            for char in line:
                game.write(str(char))
                game.write(',')
            game.write('\n')


def smartMove(opponent, word):
    board = gameState(opponent)
    word = word.upper()
    letters = list(word)
    choices = []
    for direction in ['H', 'V']:
        dirVec = {'H': 0, 'V': 0, direction: 1}
        for i in range(NUM_ROWS_COLS):
            for j in range(NUM_ROWS_COLS - len(word)):
                pass


def newGame(opponent):
    board = blankBoard()
    with open(f'{opponent}_game.txt', 'w') as game:
        for line in board:
            for char in line:
                game.write(str(char))
                game.write(',')
            game.write('\n')


# To check words with a given set of letters
# Use * for blanks
#   Input: letters [str] (the available letters, may be more or less than 7 letters)
#   Returns: words [list] (a list of all possible words)
def inMyLetters(letters):
    myLetters = list(letters.upper())
    wordlist = wordList()
    words = []
    for word in wordlist:
        copyLetters = myLetters.copy()
        inLetters = True
        for letter in word:
            if letter in copyLetters:
                copyLetters.remove(letter)
            elif '*' in copyLetters:
                copyLetters.remove('*')
            else:
                inLetters = False
                break
        if inLetters:
            words.append(word)
    return words


def letterRun(letterRun, others=''):
    wordlist = wordList()
    otherletters = list(others.upper())
    words = []
    for word in wordlist:
        if letterRun.upper() in word:
            addToList = True
            if others != '':
                othercopy = otherletters.copy()
                tempList = word.split(letterRun.upper())
                for i in tempList:
                    for letter in i:
                        if letter not in othercopy:
                            addToList = False
                            break
                        othercopy.remove(letter)
                    if not addToList:
                        break
            if addToList:
                words.append(word)
    return words


def main():
    # word = [("Z", "DW"), ("O", 0), ("A", "TL")]
    # board = scrabbleBoard()
    # *********************************************
    longWords = []
    myLetters = 'rtkhxi*v'
    run = ''
    for word in inMyLetters(myLetters):
        print(word)
        if len(word) >= 7:
            longWords.append(word)
    print("***********************\nLong words:")
    for word in longWords:
        print(word)
    # *********************************************
    if run != '':
        for word in letterRun(run, myLetters):
            print(word)
    # ***************************************************
    opponent = 'mumar'
    letters = 'vtiietn'
    bm = bestMove(opponent, letters)
    print(bm)
    if input('Make this move? (y/n): ').lower() == 'y':
        makeMove(opponent, bm[0], bm[1], bm[2])
    # ***************************************************


main()

# **************************************************
# with open('both_game.txt', 'w') as game:
#     board=blankBoard()
#     for line in board:
#         for char in line:
#             game.write(str(char))
#             game.write(',')
#         game.write('\n')
# ***************************************************
# makeMove('mumar', 'hide', 'h', (7,6))
# print(turnScore('FUSE', 'FUSE', 'H', (14, 11), gameState('mumar')))
# newGame('mumar')
# smartMove('mumar', 'whatever')
# print(wordFitsOnBoard(gameState('mumar'), 'FUSE', 'H', (14, 10)))
