import json
f = open("../test/answer.json")
temp = json.load(f)
for x in temp:
    prev = 0
    for i in temp[x]:
        print(x)
        print(i[0], i[1])
        assert i[0] >= prev
        prev = i[1]
