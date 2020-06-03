import json
f = open("../test/answer.json")
temp = json.load(f)
for x in temp:
    prev = 0
    for i in temp[x]:
        print(i[0], prev)
        assert i[0] >= prev
        prev = i[1]
