import pandas as pd
import numpy as np
import random

sat_positions = [[]]*40
for i in range(40):
    sat_positions[i] = []



with open('../input_data/sat_positions.txt') as sats:
    for i in range(40):
        for j in range(40):
            line = sats.readline()
            entry = line.split(',')
    
            dic = {"sat_id": int( entry[0]), "orbit_id" : int( entry[1]), "sat_orbit_id" : int( entry[2]),
            "lat" : float( entry[3]), "lon": float(entry[4]), "alt" : float(entry[5][0:-2])}
            sat_positions[i].append(dic)

vals_lis = []

with open('../input_data/valid_isls.txt') as vals:
    for i in range(340960):
        line = vals.readline()
        entry = line.split(',')
        entry[0] = int(entry[0])
        entry[1] = int(entry[1])
        entry[2] = float(entry[2][:-1])
        vals_lis.append(entry)

print(vals_lis[0])
sats = [0]*1601
rang = 340960
connected = 0
with open('../output_data/sat_links.txt','w') as out:
    while connected < 1500:
        i = random.randrange(0,rang)
        c = vals_lis[i]
        if sats[int(c[0])] < 4 and sats[int(c[1])] < 4 and c[2] > 3437 :
            sats[int(c[0])]+=1
            sats[int(c[1])]+=1
            if sats[int(c[0])]==4:
                connected+=1
            if sats[int(c[1])]==4:
                connected+=1
            outt = str(c[0]) + ',' + str(c[1]) + '\n' 
            out.writelines(outt)
        rang-=1
        vals_lis.remove(c)
        print(connected, len(vals_lis),i, rang)

    


links = []

"""
with open('../output_data/sat_links.txt','w') as out:
    for i in range(40):
        for j in range(40):
            x = sat_positions[i][j].get('sat_id')
            
            
            a = sat_positions[i][(j+1)%40].get('sat_id')
            b = sat_positions[(i+1)%40][j].get('sat_id')

            out1 = str(x) + ',' + str(a) + '\n'
            out2 = str(x) + ',' + str(b) + '\n'

            out.writelines(out1)
            out.writelines(out2)

"""
