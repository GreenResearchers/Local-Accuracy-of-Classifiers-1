import Calculation
import Input
import VDM
import CarHDVM

def HVDM_nersery():


    # Nursery Data Evaluation

    f=open("Nursery.data","r")
    f2=open("DistanceNersery.data","w+")
    attribute=["parents","has_nurs","form","children","housing","finance","social","health"]
    value=[["usual", "pretentious", "great_pret"],
    ["proper", "less_proper", "improper", "critical", "very_crit"],
    ["complete", "completed", "incomplete", "foster"],
    ["1", "2", "3", "more"],
    ["convenient", "less_conv", "critical"],
    ["convenient", "inconv"],
    ["nonprob", "slightly_prob", "problematic"],
    ["recommended", "priority", "not_recom"]]
    att=attribute.__len__()
    inst=12960
    class_num=att



    data=Input.read(f,att,inst)                                          # input read from file
    #print(data)

    na_count = Calculation.na_calculation(data, value,att)         # nax count
    #print(na_count)

    nac_count=Calculation.nac_calculation(attribute,data,value,class_num)        # naxc_count

    #print(nac_count)

    distance=VDM.vdm_nominal_distance(attribute,value,na_count,nac_count,class_num)

    for x in distance.keys():
        f2.write(x+":")
        for i in range(distance[x].__len__()):
            f2.write(" "+str(distance[x][i]))
        f2.write("\n")
    f.close()
    f2.close()