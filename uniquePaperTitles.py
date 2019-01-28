import pandas as pd

sheet = pd.read_csv(r"files/pubmed_title_year.csv")

setOfTitles = set()

for i in range(len(sheet['Title']) - 1, -1, -1):
    title = sheet['Title'][i].strip()

    if title not in setOfTitles:
        setOfTitles.add(title)
    else:
        print("Non-unique title found - %s at row %d\n" % (title, i + 2))