import networkx as nx
import pandas as pd

G = nx.Graph()

YEAR_START_INDEX = 12
YEAR_END_INDEX = 16

sheetTitlesYears = pd.read_csv(r"files/pubmed_title_year.csv")
sheetAuthors = pd.read_csv(r"files/pubmed_result.csv")

authorsToPapers = {}

for k in range(len(sheetAuthors['Authors']) - 1, -1, -1):
    authorList = sheetAuthors['Authors'][k]
    authors = authorList.split(",")

    for i in range(len(authors)):
        authors[i] = authors[i].split(";")[0].strip().replace(".", "")

    if "et al" in authors:
        authors.remove("et al")

    for author in set(authors): # authors must be unique for a single paper
        if author not in authorsToPapers:
            authorsToPapers[author] = []

        authorsToPapers[author].append(k) # we store indexes of the papers!

for value in authorsToPapers.values():
    if len(value) > 1:
        for i in range(len(value) - 1):
            sourcePaper = sheetTitlesYears['Title'][value[i]].strip() + "_" + str(value[i]) + "_" + sheetTitlesYears['Year'][value[i]][YEAR_START_INDEX:YEAR_END_INDEX]

            for j in range(i + 1, len(value)):
                destinationPaper = sheetTitlesYears['Title'][value[j]].strip() + "_" + str(value[j]) + "_" + sheetTitlesYears['Year'][value[j]][YEAR_START_INDEX:YEAR_END_INDEX]

                if not G.has_edge(sourcePaper, destinationPaper):
                    G.add_edge(sourcePaper, destinationPaper)


# nx.write_gml(G, "files/papersNetwork.gml") # for writing into GML file

nodeData = {
    'Id': [],
    'Label': []
}

labelToId = {}
nodeLabels = list(G.nodes)

for i in range(len(nodeLabels)):
    nodeData['Id'].append(i)
    nodeData['Label'].append(nodeLabels[i])

    labelToId[nodeLabels[i]] = i  # for creating the edges csv file

nodeDataFrame = pd.DataFrame(nodeData, columns=['Id', 'Label'])
nodeDataFrame.to_csv("files/nodePapersNetwork.csv", index=False)

edgeData = {
    'Source': [],
    'Target': [],
    'Type': []
}

for authors, _ in G.edges.items():
    edgeData['Source'].append(labelToId[authors[0]])
    edgeData['Target'].append(labelToId[authors[1]])
    edgeData['Type'].append('Directed')

edgeDataFrame = pd.DataFrame(edgeData, columns=['Source', 'Target', 'Type'])
edgeDataFrame.to_csv("files/edgePapersNetwork.csv", index=False)