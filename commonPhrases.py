import pandas as pd

toSkip = ['and', 'or', 'in', 'the', 'a', 'an', 'is', 'on', 'under', 'of', 'to', 'but', 'its', 'with']
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
    for word in words:
        word = word.lower()

        if word in toSkip:
            if newWord == '':
                continue

            newWordKey = ''.join(newWord.split())

            if newWordKey not in phraseToName:
                phraseToName[newWordKey] = newWord
                phraseToCount[newWordKey] = 1
            else:
                phraseToCount[newWordKey] += 1

            newWord = ''
        else:
            newWord += ' ' + word

phraseToCount = {k: v for k, v in
                    sorted(phraseToCount.items(), key=lambda x: x[1], reverse=True)}

file = open('files/commonPhrases.txt', 'w+')

for key, value in phraseToCount.items():
    if len(phraseToName[key].split()) > 1:
        file.write(phraseToName[key] + ': ' + str(value) + '\n')

file.close()
