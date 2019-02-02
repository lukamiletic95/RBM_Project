import pandas as pd
import matplotlib.pyplot as plt

journalToYear = {}

sheet = pd.read_csv(r"files/pubmed_journals.csv")

for journalInfo in sheet['Journals']:
    journalName = journalInfo.split('.')[0].strip()
    journalYear = journalInfo.split('.')[1].strip()

    if journalName not in journalToYear:
        journalToYear[journalName] = {}

    if journalYear not in journalToYear[journalName]:
        journalToYear[journalName][journalYear] = 1
    else:
        journalToYear[journalName][journalYear] += 1

for journal in journalToYear.keys():
    journalToYear[journal] = {k: v for k, v in
                                sorted(journalToYear[journal].items(), key=lambda x: x[1])}


x = list(journalToYear['PLoS One'].keys())
y = list(journalToYear['PLoS One'].values())

plt.plot(x, y)
plt.xlabel('Year')
plt.ylabel('Number of papers')
plt.show()


file = open("files/journalsPerYear.txt", "w+")

for key, value in journalToYear.items():
    file.write("*** " + key + " ***\n")

    for key1, value1 in value.items():
        file.write(str(key1) + ": " + str(value1) + "\n")

    file.write('\n')

file.close()