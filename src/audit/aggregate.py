import csv
from pprint import pprint

data = "./data/restaurants.tsv"
aggregates = {}

def aggregate(dictreader):
        
    for col in dictreader.fieldnames:
        aggregates[col] = {}

    for row in dictreader:
        for col in aggregates.keys():
            cell = row[col]
            aggregates[col][cell] = aggregates[col].get(cell,0)+1

def aggregateCol(column,dictreader):
    for row in dictreader:
        cell = row[column]
        aggregates[cell] = aggregates.get(cell,0)+1

print("GO\n\n")
with open(data,newline='') as f:
    r =  csv.DictReader(f,delimiter="\t",quotechar='"')
    #aggregate(r)
    aggregateCol("city",r)

pprint(aggregates)