import math
def vdm_nominal_distance(attribute, value, individual_count, nac_count,class_num):

    class_number = value[class_num-1].__len__()
    distance ={}
    d=0;
    for i in range(attribute.__len__()-1):
        for j in range(value[i].__len__()):
            x = value[i][j]
            probability=list()
            for m in range(value[i].__len__()):
                y=value[i][m]
                d = float(0.0)
                if x != y:
                    s = 1
                    for k in range(class_number):
                        nax = int(individual_count[x])
                        naxc = int(nac_count[x][k + s])
                        nay = int(individual_count[y])
                        nayc = int(nac_count[y][k + s])
                        p = abs((naxc / nax) - (nayc / nay))
                        d += round(math.sqrt(pow(p, 2)),2)
                        s += 1
                probability.append(y)
                probability.append(d)
            distance[x] = probability
    return distance
