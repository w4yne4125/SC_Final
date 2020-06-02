import json
import numpy as np
dic = {}
for i in range(1, 1501):
    path = f"../test/{i}/output.txt"
    ans_list = []
    with open(path, 'r') as f:
        for line in f:
            ls = (tuple(map(float, line.split(" "))))
            #ls[2] = int(ls[2])
            ans_list.append(ls)
    assert len(ans_list) >= 10
    dic[f"song_id{i}"] = ans_list


with open('../test/result.json', 'w') as fp:
    json.dump(dic, fp, indent=4)

with open("../test/result.json", 'r') as json_file:
    temp = json.loads(json_file.read())
print(type(temp['song_id1'][0]))
