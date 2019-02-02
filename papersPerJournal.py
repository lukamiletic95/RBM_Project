import pandas as pd
import matplotlib.pyplot as plt

sheet = pd.read_csv(r"files/pubmed_journals.csv")

papersPerJournal = {}

for journalInfo in sheet['Journals']:
    journal = journalInfo.split(".")[0].strip()

    if journal not in papersPerJournal:
        papersPerJournal[journal] = 1
    else:
        papersPerJournal[journal] += 1

papersPerJournal = {k: v for k, v in sorted(papersPerJournal.items(), key=lambda x: x[1], reverse=True)}

sumPerJournals = 0
for value in papersPerJournal.values():
    sumPerJournals += value

file = open("files/papersPerJournal.txt", "w+")

file.write("Average number of papers per journal: " + str(sumPerJournals / len(papersPerJournal)) + "\n\n")

for key, value in papersPerJournal.items():
    file.write(key + ": " + str(value) + "\n")

file.close()

papersPerJournalAppearances = {}
for value in papersPerJournal.values():
    if value not in papersPerJournalAppearances:
        papersPerJournalAppearances[value] = 1
    else:
        papersPerJournalAppearances[value] += 1

x = list(papersPerJournalAppearances.keys())
y = list(papersPerJournalAppearances.values())

plt.plot(x, y)
plt.xlabel('Papers per journal')
plt.ylabel('Number of journals')
plt.show()