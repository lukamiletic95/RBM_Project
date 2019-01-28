import pandas as pd

sheet = pd.read_csv(r"files/pubmed_result.csv")

numAuthors = 0

for authorList in sheet['Authors']:
    authors = authorList.split(",")

    for i in range(len(authors)):
        authors[i] = authors[i].split(";")[0].strip().replace(".", "")

    if "et al" in authors:
        authors.remove("et al")

    numAuthors += len(set(authors))

print("Average number of authors per paper: %.2f" % (numAuthors / len(sheet['Authors'])))