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

# adding attribute for journals

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

# adding attribute for journals

# adding attribute for phrases

toSkip = ['and', 'or', 'in', 'the', 'a', 'an', 'is', 'on', 'under', 'of', 'to', 'but', 'its', 'with', 'for', 'by', 'as', 'via', 'at']
characters = [',', '(', ')', '[', ']', ':', '?', '!', '.']

sheetAuthors = pd.read_csv(r"files/pubmed_result.csv")
sheetTitle = pd.read_csv(r"files/pubmed_title_year.csv")

phraseToName = {}
phrasesPerAuthor = {}

for i in range(len(sheetTitle['Title'])):
    title = sheetTitle['Title'][i]
    authors = sheetAuthors['Authors'][i].split(",")

    for i in range(len(authors)):
        authors[i] = authors[i].split(";")[0].strip().replace(".", "")

    if "et al" in authors:
        authors.remove("et al")

    authors = set(authors)

    for author in authors:
        if author not in phrasesPerAuthor:
            phrasesPerAuthor[author] = {}

    for character in characters:
        title = title.replace(character, '')

    words = title.split(' ')

    newWord = ''
    numWords = 0
    for word in words:
        word = word.lower()

        if word in toSkip:
            continue
        else:
            numWords += 1
            newWord += ' ' + word

            if numWords == 2:
                newWordKey = ''.join(newWord.split())

                if newWordKey not in phraseToName:
                    phraseToName[newWordKey] = newWord

                for author in authors:
                    if newWordKey not in phrasesPerAuthor[author]:
                        phrasesPerAuthor[author][newWordKey] = 1
                    else:
                        phrasesPerAuthor[author][newWordKey] += 1

                newWord = newWord.split(' ')[1]
                numWords = 1

for key in phrasesPerAuthor.keys():
    phrasesPerAuthor[key] = {k: v for k, v in
                                sorted(phrasesPerAuthor[key].items(), key=lambda x: x[1], reverse=True)}

# adding attribute for phrases

nx.write_gml(G, "files/collaborationNetwork.gml")  # for writing into GML file

nodeData = {
    'Id': [],
    'Label': [],
    'TopJournal': [],
    'TopPhrase': []
}

labelToId = {}
nodeLabels = list(G.nodes)

for i in range(len(nodeLabels)):
    nodeData['Id'].append(i)
    nodeData['Label'].append(nodeLabels[i])

    topJournals = list(authorsDictionary[nodeLabels[i]].keys())
    topJournalsTxt = ""
    for j in range(len(topJournals)):
        topJournalsTxt += topJournals[j] + " || "
        if j == 2:
            break
    nodeData['TopJournal'].append(topJournalsTxt)

    topPhrases = list(phrasesPerAuthor[nodeLabels[i]].keys())
    topPhrasesTxt = ""
    for j in range(len(topPhrases)):
        topPhrasesTxt += phraseToName[topPhrases[j]] + " || "
        if j == 2:
            break
    nodeData['TopPhrase'].append(topPhrasesTxt)

    labelToId[nodeLabels[i]] = i  # for creating the edges csv file

nodeDataFrame = pd.DataFrame(nodeData, columns=['Id', 'Label', 'TopJournal', 'TopPhrase'])
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
