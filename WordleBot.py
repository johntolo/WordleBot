from collections import Counter
with open("answers.txt","r") as answerfile: answers = answerfile.readlines()
with open("words.txt","r") as answerfile: words = answerfile.readlines()

def solveWordle():
    with open("answers.txt","r") as answerfile: answers = answerfile.readlines()
    with open("words.txt","r") as answerfile: words = answerfile.readlines()
    allAnswers = answers.copy()
    allAnswers = [i.strip() for i in allAnswers]

    bestWords = rankWords(allAnswers)
    bestWordsCopy = bestWords.copy()
    print()
    print("THESE ARE MY TOP 10 CHOICES:")
    j = 0
    for elem in bestWords:
        if j == 9:
            print(str(j+1) + ": " + elem[0] + "     Word Score: " + str(elem[1]))
            break
        print(" " + str(j+1) + ": " + elem[0] + "     Word Score: " + str(elem[1]))
        j += 1
    guess = ""
    wordsFiltered = [i.strip() for i in words]
    count = 0
    while True:
        count += 1
        print()
        guess = input("Guess #" + str(count) + ": ")
        while isValid(guess) == False or guess not in wordsFiltered:
            print("Invalid word, guess again")
            print()
            guess = input("Guess #" + str(count) + ": ")
        result = input("What's the information about the word (g/y/n)? ")
        while isValidInfo(result) == False:
            print("Invalid information, try again")
            result = input("What's the information about the word (g/y/n)? ")
        if result == "ggggg":
            print()
            print("WordleBot got the word in " + str(count) + " guesses")
            break
        result = list(result)
        if count == 6:
            print()
            print("WordleBot couldn't get the word")
            break
        filtered = filterList(answers, guess, result)
        filtered = [i.strip() for i in filtered]
        answers = filtered

        print()
        print(str(len(filtered)) + " POSSIBLE WORDS:")
        print(', '.join(filtered))

        final = ()
        # if len(filtered) < 16:
        #     print(str(len(filtered)) + ": ranked by elimination")
        #     final = rankByElimination(filtered, bestWordsCopy)
        if len(filtered) < 500:
            print(str(len(filtered)) + ": ranked by remaining words")
            final = rankByRemainingWords(filtered)
        else:
            print(str(len(filtered)) + ": ranked by normal")
            final = rankWords(filtered)
        print()
        print("WORDLEBOT'S TOP CHOICES:")
        j = 0
        for elem in final:
            if j == 9:
                print(str(j+1) + ": " + elem[0] + "     Word Score: " + str(elem[1]))
            else:
                print(" " + str(j+1) + ": " + elem[0] + "     Word Score: " + str(elem[1]))
            if j == 9 or j == len(final):
                break
            j += 1

def WordleAverage():
    with open("answers.txt","r") as answerfile: answers = answerfile.readlines()
    with open("words.txt","r") as answerfile: words = answerfile.readlines()
    #dictWords = {}
    sum = 0
    nums = 0
    answers = [i.strip() for i in answers]
    for word in answers:
        if word[0] != 'h':
            continue
        updateAnswers = answers.copy()
        count = 0
        while True:
            count += 1
            bestWords = ()
            if len(updateAnswers) > 500:
                bestWords = rankWords(updateAnswers)
            #elif len(updateAnswers) < 50:
                #bestWords = rankByElimination(updateAnswers, answers)
            else:
                bestWords = rankByRemainingWords(updateAnswers)
            guess = bestWords[0][0]
            result = getResult(guess, word)
            if result == "ggggg":
                #dictWords[word] = count
                sum += count
                break
            result = list(result)
            if count == 6:
                #dictWords[word] = 7
                sum += 7
                break
            filtered = filterList(updateAnswers, guess, result)
            filtered = [i.strip() for i in filtered]
            updateAnswers = filtered
        nums += 1
        print(word + ": " + str(count) + "  " + str(sum/nums))
    return sum

def filterList(wordList, word, result):
    returnList = wordList.copy()
    dictGreen = {}
    dictYellow = {}
    grey = list()
    i = 0
    while i < 5:
        if result[i] == 'g':
            dictGreen[word[i]] = i
        elif result[i] == 'y' and word[i]:
            dictYellow[word[i]] = i
        elif result[i] == 'n' and word[i] not in dictGreen:
            if word[i] not in dictYellow:
                grey.append(word[i])
        i += 1
    for elem in wordList:
        flag = 1
        for letter in grey:
            if letter in elem and letter not in dictGreen:
                flag = 0
        for i in dictGreen:
            if elem[dictGreen[i]] != i:
                flag = 0
        for i in dictYellow:
            if elem[dictYellow[i]] == i or i not in elem:
                flag = 0
        if flag == 0:
            returnList.remove(elem)
    return returnList

def rankWords(wordList):
    counters = Counter()
    for word in answers:
        counters.update(word)
    scores = {}
    for word in wordList:
        scores[word] = 0
        score = 0
        dupes = list()
        for letter in word:
            if word.count(letter) >= 2:
                if letter not in dupes:
                    dupes.append(letter)
            else:
                score += counters.get(letter)
        for dupe in dupes:
            score += counters.get(dupe)
        scores[word] += score
    sortedDict = sorted(scores.items(), key=lambda x:x[1])
    sortedDict.reverse()
    return sortedDict

def rankByRemainingWords(wordList):
    normalRanked = rankWords(wordList)
    normalDict = {}
    normalDict = convertTup(normalRanked, normalDict)
    dictWords = {}
    for word in wordList:
        dictWords[word] = 1
        for word2 in wordList:
            result = list()
            if word2 == word:
                continue
            i = 0
            while i < 5:
                if word[i] == word2[i]:
                    result.append('g')
                if word[i] != word2[i] and word[i] in word2:
                    result.append('y')
                if word[i] not in word2:
                    result.append('n')
                i += 1
            filtered = filterList(wordList, word, result)
            dictWords[word] += len(filtered)
        dictWords[word] = normalDict[word] / dictWords[word]
    sortedDict = sorted(dictWords.items(), key=lambda x:x[1])
    sortedDict.reverse()
    return sortedDict

def rankByElimination(remainingWords, bestWords):
    with open("answers.txt","r") as answerfile: answers = answerfile.readlines()
    with open("words.txt","r") as answerfile: words = answerfile.readlines()
    words = [i.strip() for i in words]
    dictLast4Same = {}
    last4Lists = {}
    for word in remainingWords:
        last4Count = 0
        last4 = word[1:4]
        if(dictLast4Same.__contains__(last4)):
            last4Count += dictLast4Same[last4]
            last4Lists[last4].append(word[0])
            dictLast4Same[last4] += 1
        else:
            dictLast4Same[last4] = 0
            last4Lists[last4] = list(word[0])
            dictLast4Same[last4] += 1
        if(dictLast4Same[last4] >= 4):
            wordScores = {}
            for i in range(len(words)):
                wordScores[words[i]] = 0
                #bestWords[i][1] = 0
                dupeCount = []
                for letter in words[i]:
                    if(letter in dupeCount):
                        wordScores[words[i]] -= 25
                    dupeCount.append(letter)
                    #print(words[i])
                    if words[i] == "bunch":
                        print(letter + ": " + last4Lists[last4])
                    if letter in last4Lists[last4]:
                        wordScores[i] += 50
            sortedDict = sorted(wordScores.items(), key=lambda x:x[1])
            sortedDict.reverse()
            return sortedDict
    return rankByRemainingWords(remainingWords)

def getResult(word, answer):
    yellowList = {}
    answerList = convertString(answer)
    result = ""
    i = 0
    while i < 5:
        yellowList[word[i]] = 0
        if word[i] == answer[i]:
            result += "g"
        if word[i] != answer[i] and word[i] in answerList:
            yellowList[word[i]] += 1
            if yellowList[word[i]] > answer.count(word[i]):
                result += "n"
            else:
                result += "y"
        if word[i] not in answerList:
            result += "n"
        i += 1
    return result

def isValid(word):
    if len(word) != 5:
        return False
    return True

def isValidInfo(info):
    if len(info) != 5:
        return False
    for char in info:
        if char not in {'g','y','n'}:
            return False
    return True

def convertTup(tup, di):
    di = dict(tup)
    return di

def convertString(string):
    list1 = []
    list1[:0] = string
    return list1