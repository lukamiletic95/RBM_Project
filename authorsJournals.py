import pandas as pd

sheetJournals = pd.read_csv(r"files/pubmed_journals.csv")
sheetAuthors = pd.read_csv(r"files/pubmed_result.csv")

authorsDictionary = {}

for k in range(len(sheetAuthors['Authors'])):
    authors = sheetAuthors['Authors'][k].split(",")
    journal = sheetJournals['Journals'][k].split(".")[0].strip()

    for i in range(len(authors)):
        authors[i] = authors[i].split(';')[0].strip().replace('.','')

    if 'et al' in authors:
        authors.remove('et al')

    for i in range(len(authors)):

        if authors[i] not in authorsDictionary:
            authorsDictionary[authors[i]] = {}

        if journal in authorsDictionary[authors[i]]:
            authorsDictionary[authors[i]][journal] += 1
        else:
            authorsDictionary[authors[i]][journal] = 1

for author in authorsDictionary.keys():
    authorsDictionary[author] = {k: v for k, v in
                                sorted(authorsDictionary[author].items(), key=lambda x: x[1], reverse=True)}

file = open("files/authorsJournals.txt", "w+")

for key, value in authorsDictionary.items():
    file.write("*** " + key + " ***\n")

    for key1, value1 in value.items():
        file.write(key1 + ": " + str(value1) + "\n")

    file.write('\n')

file.close()