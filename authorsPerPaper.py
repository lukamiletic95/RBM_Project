import pandas as pd
import matplotlib.pyplot as plt

sheet = pd.read_csv(r"files/pubmed_result.csv")

numAuthors = 0

authorsPerPaper = {}

for authorList in sheet['Authors']:
    authors = authorList.split(",")

    for i in range(len(authors)):
        authors[i] = authors[i].split(";")[0].strip().replace(".", "")

    if "et al" in authors:
        authors.remove("et al")

    numAuthorsCurrentPaper = len(set(authors))

    numAuthors += numAuthorsCurrentPaper

    if numAuthorsCurrentPaper not in authorsPerPaper:
        authorsPerPaper[numAuthorsCurrentPaper] = 1
    else:
        authorsPerPaper[numAuthorsCurrentPaper] += 1


authorsPerPaper = {k: v for k, v in sorted(authorsPerPaper.items(), key=lambda x: x[0], reverse=True)}

file = open("files/authorsPerPaper.txt", "w+")

file.write("Average number of authors per paper: %.2f" % (numAuthors / len(sheet['Authors'])) + "\n\n")

for key, value in authorsPerPaper.items():
    file.write(str(key) + ": " + str(value) + "\n")

file.close()

x = list(authorsPerPaper.keys())
y = list(authorsPerPaper.values())

plt.plot(x, y)
plt.xlabel('Number of authors')
plt.ylabel('Number of papers')
plt.show()