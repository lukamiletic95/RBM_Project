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

# nx.write_gml(G, "files/collaborationNetwork.gml") # for writing into GML file

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
nodeDataFrame.to_csv("files/node.csv", index=False)

edgeData = {
    'Source': [],
    'Target': [],
    'Type': [],
    'Weight': []
}

for authors, weight in G.edges.items():
    edgeData['Source'].append(labelToId[authors[0]])
    edgeData['Target'].append(labelToId[authors[1]])
    edgeData['Type'].append('Undirected')
    edgeData['Weight'].append(weight['weight'])

edgeDataFrame = pd.DataFrame(edgeData, columns=['Source', 'Target', 'Type', 'Weight'])
edgeDataFrame.to_csv("files/edge.csv", index=False)
