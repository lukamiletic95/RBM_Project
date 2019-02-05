import pandas as pd

toSkip = ['and', 'or', 'in', 'the', 'a', 'an', 'is', 'on', 'under', 'of', 'to', 'but', 'its', 'with', 'for', 'by', 'as', 'via', 'at']
characters = [',', '(', ')', '[', ']', ':', '?', '!', '.']

sheet = pd.read_csv(r"files/pubmed_title_year.csv")

phraseToName = {}
phraseToCount = {}

for i in range(len(sheet['Title'])):
    title = sheet['Title'][i]

    for character in characters:
        title = title.replace(character, '')

    words = title.split(' ')

    newWord = ''
    numWords = 0
    for word in words:
        if word == '':
            continue

        word = word.lower()

        if word in toSkip:
            continue
        else:
            numWords += 1
            if newWord != '':
                newWord += ' '
            newWord += word

            if numWords == 2:
                newWordKey = ''.join(newWord.split())

                if newWordKey not in phraseToName:
                    phraseToName[newWordKey] = newWord
                    phraseToCount[newWordKey] = 1
                else:
                    phraseToCount[newWordKey] += 1

                newWord = newWord.split(' ')[1]
                numWords = 1

phraseToCount = {k: v for k, v in
                 sorted(phraseToCount.items(), key=lambda x: x[1], reverse=True)}

file = open('files/commonPhrasesOfTwo.txt', 'w+')

for key, value in phraseToCount.items():
    file.write(phraseToName[key] + ': ' + str(value) + '\n')

file.close()
