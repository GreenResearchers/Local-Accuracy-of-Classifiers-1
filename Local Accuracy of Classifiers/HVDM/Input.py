import Calculation

def read(f,att,inst):
    #Declaring list of list of size att*inst
    data = []
    for i in range(att):
        data.append([] * inst)
    #Taking Nursery data into list of list named data
    for x in f:
        y = x.split(",")
        y[-1] = y[-1].strip()
        for i in range(att):
            data[i].append(y[i])
    return data
