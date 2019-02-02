import pandas as pd
import matplotlib.pyplot as plt

sheetJournals = pd.read_csv(r"files/pubmed_journals.csv")
sheetAuthors = pd.read_csv(r"files/pubmed_result.csv")

authorsPerJournal = {}

for k in range(len(sheetAuthors['Authors'])):
    authors = sheetAuthors['Authors'][k].split(",")
    journal = sheetJournals['Journals'][k].split(".")[0].strip()

    for i in range(len(authors)):
        authors[i] = authors[i].split(';')[0].strip().replace('.','')

    if 'et al' in authors:
        authors.remove('et al')

    if journal not in authorsPerJournal:
        authorsPerJournal[journal] = len(authors)
    else:
        authorsPerJournal[journal] += len(authors)

authorsPerJournal = {k: v for k, v in sorted(authorsPerJournal.items(), key=lambda x: x[1], reverse=True)}

sumPerJournals = 0
for value in authorsPerJournal.values():
    sumPerJournals += value

file = open("files/authorsPerJournal.txt", "w+")

file.write("Average number of authors per journal: " + str(sumPerJournals / len(authorsPerJournal)) + "\n\n")

for key, value in authorsPerJournal.items():
    file.write(key + ": " + str(value) + "\n")

file.close()

authorsPerJournalAppearances = {}
for value in authorsPerJournal.values():
    if value not in authorsPerJournalAppearances:
        authorsPerJournalAppearances[value] = 1
    else:
        authorsPerJournalAppearances[value] += 1

x = list(authorsPerJournalAppearances.keys())
y = list(authorsPerJournalAppearances.values())

plt.plot(x, y)
plt.xlabel('Authors per journal')
plt.ylabel('Number of journals')
plt.show()