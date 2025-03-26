import json

with open('zastavky.txt', 'r', encoding='utf-8') as f:
    data=json.load(f)

output=[]
for x in data["stopGroups"]:
    for zast in x["stops"]:
        if zast["lines"]==[]:
            continue
        plat = zast.get("platform", '')
        d={"altIdosName": zast["altIdosName"], "platform":plat,"gtfsIds":zast["gtfsIds"][0], "coords": [zast['lat'], zast['lon']], "lines":[]}
        for linka in zast["lines"]:
            if "isNight" in linka and linka["isNight"] is True:
                continue
            # linkyst.append('{0}{1}{2}'.format(linka["name"],"->",linka["direction"]))
            d["lines"].append([linka["name"], linka["direction"]])            
        output.append(d)

# with open("outp_zast.json", 'w', encoding='utf-8') as output_file:
#     json.dump(output, output_file)
with open("outp_zast.txt", 'w', encoding='utf-8') as output_file:
    output_file.write(str(output).replace("'", '"'))

print('num stops =', len(output))
# print(data["stopGroups"][0]["stops"][0].keys())
