import json
dic = {}
for i in range(1, 501):
    path = f"../train/{i}/combine.txt"
    ans_list = []
    with open(path, 'r') as f:
        for line in f:
            ans_list.append(list(map(float, line.split(" "))))
    dic[f"song_id{i}"] = ans_list

with open('../train/result.json', 'w') as fp:
    json.dump(dic, fp)
