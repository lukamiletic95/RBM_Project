import pandas as pd

toSkip = ['and', 'or', 'in', 'the', 'a', 'an', 'is', 'on', 'under', 'of', 'to', 'but', 'its', 'with', 'for', 'by', 'as', 'via', 'at']
characters = [',', '(', ')', '[', ']', ':', '?', '!', '.']

sheetAuthors = pd.read_csv(r"files/pubmed_result.csv")
sheetTitle = pd.read_csv(r"files/pubmed_title_year.csv")

phraseToName = {}
phrasesPerAuthor = {}

for i in range(len(sheetTitle['Title'])):
    title = sheetTitle['Title'][i]
    authors = sheetAuthors['Authors'][i].split(",")

    for i in range(len(authors)):
        authors[i] = authors[i].split(";")[0].strip().replace(".", "")

    if "et al" in authors:
        authors.remove("et al")

    authors = set(authors)

    for author in authors:
        if author not in phrasesPerAuthor:
            phrasesPerAuthor[author] = {}

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

                for author in authors:
                    if newWordKey not in phrasesPerAuthor[author]:
                        phrasesPerAuthor[author][newWordKey] = 1
                    else:
                        phrasesPerAuthor[author][newWordKey] += 1

                newWord = newWord.split(' ')[1]
                numWords = 1

for key in phrasesPerAuthor.keys():
    phrasesPerAuthor[key] = {k: v for k, v in
                                sorted(phrasesPerAuthor[key].items(), key=lambda x: x[1], reverse=True)}

file = open("files/phrasesPerAuthor.txt", "w+")

for key, value in phrasesPerAuthor.items():
    file.write("*** " + key + " ***\n")

    for key1, value1 in value.items():
        file.write(phraseToName[key1] + ": " + str(value1) + "\n")

    file.write('\n')

file.close()