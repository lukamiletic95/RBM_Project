import pandas as pd

toSkip = ['and', 'or', 'in', 'the', 'a', 'an', 'is', 'on', 'under', 'of', 'to', 'but']
characters = [',', '(', ')', '[', ']', ':', '?', '!', '.']

sheet = pd.read_csv(r"files/pubmed_title_year.csv")

phraseToName = {}
phraseToCount = {}

for i in range(len(sheet['Title'])):
    title = sheet['Title'][i]

    for character in characters:
        title = title.replace(character, '')

    words = title.split(' ')

    newWord = ""
    for word in words:
        if word in toSkip:
            newWordLower = "".join(newWord.split()).lower()

            if newWordLower not in phraseToName:
                phraseToName[newWordLower] = newWord
                phraseToCount[newWordLower] = 1
            else:
                phraseToCount[newWordLower] += 1

        else:
            newWord += ' ' + word

phraseToCount = {k: v for k, v in
                    sorted(phraseToCount.items(), key=lambda x: x[1], reverse=True)}

file = open('files/commonPhrases.txt', 'w+')

for key, value in phraseToCount.items():
    file.write(phraseToName[key] + ': ' + str(value) + '\n')

file.close()
