import csv

def getDicts(data):
    with open(data,newline='') as f:
        r =  csv.DictReader(f,delimiter="\t",quotechar='"')
        return {"meta":r,"data":[dict for dict in r]}
