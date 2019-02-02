import pandas as pd

sheet = pd.read_csv(r"files/pubmed_title_year.csv")

keywords = [line.rstrip('\n') for line in open('files/keywords.txt')]

keywordsToPapers = {}

for keyword in keywords:
    keywordsToPapers[keyword] = 0

for title in sheet['Title']:
    titleName = ("".join(title.split())).lower()

    for keyword in keywords:
        if keyword in titleName:
            keywordsToPapers[keyword] += 1

keywordsToPapers = {k: v for k, v in
                    sorted(keywordsToPapers.items(), key=lambda x: x[1], reverse=True)}

file = open('files/keywordsToPapers.txt', 'w+')

for keyword, papersCount in keywordsToPapers.items():
    file.write("*** " + keyword + " ***\n")
    file.write("Number of papers: " + str(papersCount) + "\n")
    file.write("\n\n")

file.close()
