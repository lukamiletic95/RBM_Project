import networkx as nx
import pandas as pd

G = nx.Graph()

sheet = pd.read_csv(r"files/pubmed_result.csv")

for authorList in sheet['Authors']:
    authors = authorList.split(",")

    for i in range(len(authors)):
        authors[i] = authors[i].split(";")[0].strip().replace(".", "")

    if "et al" in authors:
        authors.remove("et al")

    for i in range(len(authors) - 1):
        for j in range(i + 1, len(authors)):
            if authors[i] == authors[j]:
                continue

            if G.has_edge(authors[i], authors[j]):
                G[authors[i]][authors[j]]['weight'] += 1 / (len(set(authors)) - 1)
            else:
                G.add_edge(authors[i], authors[j])
                G[authors[i]][authors[j]]['weight'] = 1 / (len(set(authors)) - 1)

# adding Attribute

authorsDictionary = {}
sheetJournals = pd.read_csv(r"files/pubmed_journals.csv")

for k in range(len(sheet['Authors'])):
    authors = sheet['Authors'][k].split(",")
    journal = sheetJournals['Journals'][k].split(".")[0].strip()

    for i in range(len(authors)):
        authors[i] = authors[i].split(';')[0].strip().replace('.', '')

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

for author, journals in authorsDictionary.items():
    topJournal = list(journals.keys())[0]

    attributes = {author: {'topJournal': topJournal}}
    nx.set_node_attributes(G, attributes)

# adding Attribute

#nx.write_gml(G, "files/collaborationNetwork.gml")  # for writing into GML file

nodeData = {
    'Id': [],
    'Label': [],
    'TopJournal': []
}

labelToId = {}
nodeLabels = list(G.nodes)

for i in range(len(nodeLabels)):
    nodeData['Id'].append(i)
    nodeData['Label'].append(nodeLabels[i])
    nodeData['TopJournal'].append(list(authorsDictionary[nodeLabels[i]].keys())[0])

    labelToId[nodeLabels[i]] = i  # for creating the edges csv file

nodeDataFrame = pd.DataFrame(nodeData, columns=['Id', 'Label', 'TopJournal'])
nodeDataFrame.to_csv("files/node.csv", index=False)

edgeData = {
    'Source': [],
    'Target': [],
    'Type': [],
    'Weight': []
}

for authors, attributes in G.edges.items():
    edgeData['Source'].append(labelToId[authors[0]])
    edgeData['Target'].append(labelToId[authors[1]])
    edgeData['Type'].append('Undirected')
    edgeData['Weight'].append(attributes['weight'])

edgeDataFrame = pd.DataFrame(edgeData, columns=['Source', 'Target', 'Type', 'Weight'])
edgeDataFrame.to_csv("files/edge.csv", index=False)
