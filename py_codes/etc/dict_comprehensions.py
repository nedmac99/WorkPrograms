workers = ["Camden","TJ","Geo"]

romans = [{"name": worker, "house": "Rome"} for worker in workers]

#romans = [{worker: "Rome"} for worker in workers]
#Returns [{'Camden': 'Rome'}, {'TJ': 'Rome'}, {'Geo': 'Rome'}]
    
print(romans)