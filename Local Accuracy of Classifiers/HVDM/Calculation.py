from collections import defaultdict

def na_calculation(data, value,att):
    # Declaring list of list individual_count of size att*each value length in value list
    individual_count = {}

    # Pre counting of each attribute value from all instance and stored in a list of list individual_count
    for i in range(att):
        for j in range(value[i].__len__()):
            individual_count[value[i][j]]=data[i].count(value[i][j])
    return individual_count


def nac_calculation(attribute, data,value,class_num):
    nac_count = {}
    for i in range(attribute.__len__() - 1):  # i 1 to attribute number
        for j in range(data[i].__len__()):  # j 1 to all attribute value in i
            x = data[i][j]
            naxc = list()
            if x not in nac_count:
                for k in value[class_num-1]:  # k 1 to class number
                    count = 0
                    for m in range(data[i].__len__()):  # m 1 to all attribute value in i ( it works like loop j)
                        if data[i][m] == x and data[class_num-1][m] == k:  # counting number of attribute value having class k
                            count += 1
                    naxc.append(k)
                    naxc.append(count)
                nac_count[x] = naxc
    return nac_count


def modifiedprecalculation(data, value,att):
    # Declaring list of list individual_count of size att*each value length in value list
    individual_count = defaultdict(list)

    # Pre counting of each attribute value from all instance and stored in a list of list individual_count
    for i in range(att):
        for j in range(value[i].__len__()):
            individual_count[value[i][j]].append(data[i].count(value[i][j]))
    dict(individual_count)
    return individual_count
