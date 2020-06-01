def combine(ori_path, onset_path, result):
    ori = open(ori_path, 'r')
    res = open(result, 'w')
    try:
        onset = open(onset_path, 'r')
    except:
        for line in ori:
            res.write(line)
        return
    ori_list = []
    for line in ori:
        ori_list.append(list(map(float,line.split(" ")[:3])))
    onset_list = []
    for line in onset:
        onset_list.append(float(line))
    prev = 0
    for i in range(len(ori_list)):
        Min = 10000
        ans = -1
        rec = -1
        for idx in range(prev, len(onset_list)):
            x = onset_list[idx]
            if abs(x - ori_list[i][0]) < Min:
                Min = abs(x - ori_list[i][0])
                ans = x
                rec = idx
        if Min < eta and ans < ori_list[i][1]:
            ori_list[i][0] = ans
            prev = rec
    for i in range(len(ori_list)-1):
        ori_list[i][1] = min(ori_list[i][1], ori_list[i+1][0])
        if (ori_list[i][1] < ori_list[i][0]  or ori_list[i+1][0] < ori_list[i][1] ):
            print("Error")
    for x in ori_list:
        res.write(f"{x[0]} {x[1]} {x[2]}\n")


if __name__ == '__main__':
    eta = 0.3
    for i in range(1, 501):
        path = f'../train/{i}'
        ori_path = f"../train/{i}/output.txt"
        onset_path = f"../train/{i}/onset.txt"
        result = f"../train/{i}/combine.txt"
        combine(ori_path, onset_path, result)



