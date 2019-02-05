import pandas as pd

toSkip = ['and', 'or', 'in', 'the', 'a', 'an', 'is', 'on', 'under', 'of', 'to', 'but', 'its', 'with', 'for', 'by', 'as', 'via', 'at']
characters = [',', '(', ')', '[', ']', ':', '?', '!', '.']

sheetJournal = pd.read_csv(r"files/pubmed_journals.csv")
sheetTitle = pd.read_csv(r"files/pubmed_title_year.csv")

phraseToName = {}
phrasesPerJournal = {}

for i in range(len(sheetTitle['Title'])):
    title = sheetTitle['Title'][i]
    journal = sheetJournal['Journals'][i].split(".")[0].strip()

    if journal not in phrasesPerJournal:
        phrasesPerJournal[journal] = {}

    for character in characters:
        title = title.replace(character, '')

    words = title.split(' ')

    newWord = ''
    numWords = 0
    for word in words:
        word = word.lower()

        if word in toSkip:
            continue
        else:
            numWords += 1
            newWord += ' ' + word

            if numWords == 2:
                newWordKey = ''.join(newWord.split())

                if newWordKey not in phraseToName:
                    phraseToName[newWordKey] = newWord

                if newWordKey not in phrasesPerJournal[journal]:
                    phrasesPerJournal[journal][newWordKey] = 1
                else:
                    phrasesPerJournal[journal][newWordKey] += 1

                newWord = newWord.split(' ')[1]
                numWords = 1

for key in phrasesPerJournal.keys():
    phrasesPerJournal[key] = {k: v for k, v in
                                sorted(phrasesPerJournal[key].items(), key=lambda x: x[1], reverse=True)}

file = open("files/phrasesPerJournal.txt", "w+")

for key, value in phrasesPerJournal.items():
    file.write("*** " + key + " ***\n")

    for key1, value1 in value.items():
        file.write(phraseToName[key1] + ": " + str(value1) + "\n")

    file.write('\n')

file.close()