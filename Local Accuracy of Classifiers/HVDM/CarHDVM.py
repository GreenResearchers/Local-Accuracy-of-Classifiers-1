import Calculation
import Input
import VDM

def HVDM_car():

    # Car Data Evaluation

    f=open("Car.data","r")
    f2=open("DistanceCar.data","w+")
    attribute=["buying","maint","doors","persons","lug_boot","safety"]
    value=[["vhigh", "high", "med","low"],
    ["vhigh", "high", "med","low"],
    ["2", "3", "4", "5more"],
    ["2", "4", "more"],
    ["small", "med", "big"],
    ["low", "med","high"]]

    att=attribute.__len__()
    inst=1728
    class_num=int(6)

    data=Input.read(f,att,inst)                                             # input read from file

                                                                            # Car data replacing with concatenating attribute
    for i in range(attribute.__len__()):
        for j in range(inst):
            data[i][j]=data[i][j]+attribute[i]

    for i in range(att):
        for j in range(value[i].__len__()):
            value[i][j] = value[i][j] + attribute[i]
    na_count = Calculation.na_calculation(data, value,att)                  # nax count
    #print(na_count)
    nac_count=Calculation.nac_calculation(attribute,data,value,class_num)          # naxc_count
    #print(value)
    #print(nac_count)
    distance=VDM.vdm_nominal_distance(attribute,value,na_count,nac_count,class_num)

    for x in distance.keys():
        f2.write(x+":")
        for i in range(distance[x].__len__()):
            f2.write(" "+str(distance[x][i]))
        f2.write("\n")

    f.close()
    f2.close()