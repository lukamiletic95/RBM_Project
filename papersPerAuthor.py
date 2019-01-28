import pandas as pd
import matplotlib.pyplot as plt

sheet = pd.read_csv(r"files/pubmed_result.csv")

papersPerAuthor = {}

for authorList in sheet['Authors']:
    authors = authorList.split(",")

    for i in range(len(authors)):
        authors[i] = authors[i].split(";")[0].strip().replace(".", "")

    if "et al" in authors:
        authors.remove("et al")

    uniqueAuthors = set(authors)  # duplicate authors appear for a single paper

    for author in uniqueAuthors:
        if author not in papersPerAuthor:
            papersPerAuthor[author] = 1
        else:
            papersPerAuthor[author] += 1

papersPerAuthor = {k: v for k, v in sorted(papersPerAuthor.items(), key=lambda x: x[1], reverse=True)}

sumProductivity = 0
for value in papersPerAuthor.values():
    sumProductivity += value

file = open("files/papersPerAuthor.txt", "w+")

file.write("Average number of papers per author: " + str(sumProductivity / len(papersPerAuthor)) + "\n\n")

for key, value in papersPerAuthor.items():
    file.write(key + ": " + str(value) + "\n")

file.close()

papersPerAuthorAppearances = {}
for value in papersPerAuthor.values():
    if value not in papersPerAuthorAppearances:
        papersPerAuthorAppearances[value] = 1
    else:
        papersPerAuthorAppearances[value] += 1

x = list(papersPerAuthorAppearances.keys())
y = list(papersPerAuthorAppearances.values())

plt.plot(x, y)
plt.xlabel('Papers per author')
plt.ylabel('Number of authors')
plt.show()