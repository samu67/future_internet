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

links = []

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

