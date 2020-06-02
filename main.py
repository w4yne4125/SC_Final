import math
import os, json
import numpy as np

def decide_base(seg_list):
    """
    決定最小切割單位
    """
    acc = np.zeros(1000)
    for x in seg_list:
        acc[len(x)] += 1
    return min(max(np.argmax(acc), 8), 10) - 1 # 有些歌並無明顯斷點

def isTail(idx, seg_list):
    """
    是否為唱句尾端 (尚未投入應用)
    """
    if (idx == len(seg_list) - 1):
        return 1
    if (seg_list[idx+1][0][0] - seg_list[idx][-1][0] >= TailSec):
        return 1
    return 0


def predict_seg(idx, seg_list, base_length, f):
    """
    切割一段唱段
    若切出段數=1 -> 直接輸出首尾，以後端音符決定音高
    若切出段數>1 -> 先以連綴音作基本分割
    大概規則為： 0000001111100000111111000110
    ->           00000011111 00000111111 000110
    以連綴音決定
    """
    base_count = max(round(len(seg_list[idx]) / base_length), 1)
    base_len = len(seg_list[idx]) // base_count
    target = seg_list[idx]
    if base_count == 1: # basic situation
        written = 0
        continuous = [0 for i in range(len(target))]
        for i in range(len(target)):
            if continuous[i]:
               continue
            end = i+1
            while (end < len(target)):
                if (abs(target[end][1] - target[end-1][1]) <= continuous_fac ):
                    end += 1
                else:
                    break
            if end - i >= continuous_part:
                note = target[i][1]
                f.write(f"{target[0][0] - s_bias} {target[-1][0] + e_bias} {note}\n")
                written = 1
                break
        if not written: 
            cnt = 0
            acc = 0
            for i in range(len(target) // 2, len(target)):
                weight = math.sqrt(len(target) - i)
                cnt += weight
                acc += target[i][1] * weight
            note = acc / cnt
            f.write(f"{target[0][0] - s_bias} {target[-1][0] + e_bias} {note}\n")
    else:
       continuous = [0 for i in range(len(target))]
       for i in range(len(target)):
           if continuous[i]:
               continue
           end = i+1
           while (end < len(target)):
               if (abs(target[end][1] - target[end-1][1]) <= continuous_fac ):
                   end += 1
               else:
                   break
           if end - i >= continuous_part:
               for j in range(i, end):
                   continuous[j] = 1
       prev = 0
       for i in range(1, len(target)):
           if (continuous[i] - continuous[i-1] == -1): # breakpoint
               if (i - prev < min_seg_len):
                   continue
               note = target[i-1][1]
               f.write(f"{target[prev][0] - s_bias} {target[i-1][0] + e_bias} {note}\n")
               prev = i
       if prev != len(target) - 1:
           note = -1
           for i in range(prev, len(target)):
               if (continuous[i]):
                   note = round(target[i][1])
                   break
           if note == -1:
               cnt = 0
               acc = 0
               for i in range((prev + len(target)) // 2, len(target)):
                   weight = math.sqrt(len(target) - i)
                   cnt += weight
                   acc += target[i][1] * weight
               note = acc / cnt
           f.write(f"{target[prev][0] - s_bias} {target[len(target)-1][0] + e_bias} {note}\n")


def predict(dir_path, idx):
    """
    先以pitch = 0作基本分段
    """
    json_path = dir_path + f"/{idx}_vocal.json"
    with open(json_path, 'r') as json_file:
        temp = json.loads(json_file.read())
    """ zeros_connections """
    prev = 1
    while prev < len(temp):
        if not temp[prev][1]:
            for j in range(prev+1, prev+zeros_connection):
                if j == len(temp):
                    break
                if temp[j][1]: # 把0補齊from i to j-1
                    for k in range(prev, j):
                        temp[k][1] = temp[k-1][1]
            # 跳到下一個1
            while prev < len(temp) and temp[prev][1] == 0:
                prev += 1
        else:
            prev += 1

    seg_list = []
    seg = []
    prev = 0
    for x in temp:
        if x[1]:
            seg.append(x)
            prev = 1
        elif prev:
            seg_list.append(seg)
            seg = []
            prev = 0
    if len(seg):
        seg_list.append(seg)
    base_length = decide_base(seg_list)
    file_path = dir_path + "/output.txt"
    f = open(file_path, 'w')
    for i in range(len(seg_list)):
        predict_seg(i, seg_list, base_length, f)
    f.close()

def F_score(dst_file, name):
    F_COn = [0, 0, 0]
    F_COnP = [0, 0, 0]
    F_COnPOff = [0, 0, 0]
    for i in range(1, 501):
        src = open(f"../train/{i}/{i}.txt", 'r')
        try:
            dst = open(f"../train/{i}/{dst_file}", 'r')
        except:
            continue
        log = open(f"../train/{i}/{dst_file}_log", "w")
        src_list = []
        dst_list = []
        for line in src:
            src_list.append(list(map(float, line.split(" ")[:3])))
        for line in dst:
            dst_list.append(list(map(float, line.split(" ")[:4])))
        F_COn[0] += len(src_list)
        F_COn[1] += len(dst_list)
        F_COnP[0] += len(src_list)
        F_COnP[1] += len(dst_list)
        F_COnPOff[0] += len(src_list)
        F_COnPOff[1] += len(dst_list)
        for x in dst_list:
            A = 0
            B = 0
            C = 0
            for y in src_list:
                if abs(x[0] - y[0]) <= 0.05:
                    A = 1
                    if round(x[2]) == round(y[2]):
                        B = 1
                        offset = max(0.05, 0.2 * (y[1]-y[0]))
                        if abs(x[1] - y[1]) <= offset:
                            C = 1 
            if A:
                F_COn[2] += 1
            if B:
                F_COnP[2] += 1
            if C:
                F_COnPOff[2] += 1
            log.write(f"{x[0]:3.2f} {x[1]:3.2f} {x[2]:3.2f} {A} {B} {C}\n")

    score1 = 2 * F_COn[2] / (F_COn[0] + F_COn[1])
    score2 = 2 * F_COnP[2] / (F_COnP[0] + F_COnP[1])
    score3 = 2 * F_COnPOff[2] / (F_COnPOff[0] + F_COnPOff[1])
    print(f"On test {name}")
    print(f"F_COn : {F_COn[0]} {F_COn[1]} {F_COn[2]} {score1}")
    print(f"F_COnP : {F_COnP[0]} {F_COnP[1]} {F_COnP[2]} {score2}")
    print(f"F_COnPOff : {F_COnPOff[0]} {F_COnPOff[1]} {F_COnPOff[2]} {score3}")
    print(f"Overall : {0.2 * score1 + 0.6 * score2 + 0.2 * score3}")

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
            ori_list[i][0] = ans - combine_bias
            prev = rec
    for i in range(len(ori_list)-1):
        ori_list[i][1] = min(ori_list[i][1], ori_list[i+1][0])
        if (ori_list[i][1] < ori_list[i][0]  or ori_list[i+1][0] < ori_list[i][1] ):
            print("Error", ori_list[i][0], ori_list[i][1], ori_list[i+1][0])
    for x in ori_list:
        if x[1]-x[0] > refine_eta[1] or x[1]-x[0] < refine_eta[0]:
            res.write(f"{x[0]} {x[1]} {x[2]}\n")


def txt2json():
    dic = {}
    for i in range(1, 1501):
        path = f"../test/{i}/combine.txt"
        ans_list = []
        with open(path, 'r') as f:
            for line in f:
                ls = (list(map(float, line.split(" "))))
                ls[2] = round(ls[2])
                ans_list.append(ls)
        dic[f"{i}"] = ans_list
    with open('../test/answer.json', 'w') as fp:
        json.dump(dic, fp, indent=4)


if __name__ == '__main__':
    """ Configs """
    Type = 'test'
    eta = 0.1
    refine_eta = [0.01, 0.1]
    TailSec = 1
    s_bias = 0.00
    e_bias = 0.00
    combine_bias = 0.00
    continuous_fac = 0.01
    continuous_part = 3
    min_seg_len = 0      # 每一個音符最少要有幾個0.032 frame
    zeros_connection = 2 # 少於多少0的話，就把他連起來
    log = True # 是否紀錄對錯
    """ Configs """

    if Type == 'train':
        for i in range(1, 501):
            path = f'../{Type}/{i}/'
            predict(path, i)
            ori_path = f"../train/{i}/output.txt"
            onset_path = f"../train/{i}/onset.txt"
            result = f"../train/{i}/combine.txt"
            combine(ori_path, onset_path, result)
        F_score("output.txt", "ori")
        F_score("test.txt", "sample")
        F_score("combine.txt", "combine")


    if Type == 'test':
        for i in range(1, 1501):
            path = f'../{Type}/{i}/'
            predict(path, i)
            ori_path = f"../{Type}/{i}/output.txt"
            onset_path = f"../{Type}/{i}/onset.txt"
            result = f"../{Type}/{i}/combine.txt"
            combine(ori_path, onset_path, result)
        txt2json()




