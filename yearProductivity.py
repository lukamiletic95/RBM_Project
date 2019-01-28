import pandas as pd
import matplotlib.pyplot as plt

YEAR_START_INDEX = 12
YEAR_END_INDEX = 16

sheetTitlesYears = pd.read_csv(r"files/pubmed_title_year.csv")
yearProductivity = {}

for i in range(len(sheetTitlesYears['Year'])):
    year = int(sheetTitlesYears['Year'][i][YEAR_START_INDEX:YEAR_END_INDEX])
    
    if year not in yearProductivity:
        yearProductivity[year] = 1
    else:
        yearProductivity[year] += 1

x = list(yearProductivity.keys())
y = list(yearProductivity.values())

plt.plot(x, y)
plt.xlabel('Year')
plt.ylabel('Number of papers')
plt.show()

sumProductivity = 0
for value in yearProductivity.values():
    sumProductivity += value

file = open("files/yearProductivity.txt", "w+")

file.write("Average number of papers per year: " + str(sumProductivity / len(yearProductivity)) + "\n\n")

for key, value in yearProductivity.items():
    file.write(str(key) + ": " + str(value) + "\n")

file.close()
