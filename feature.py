import math
import os, json
import numpy as np


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
#{{{ F-score
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
                    if True or round(x[2]) == round(y[2]):
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
#}}}
#{{{ txt2json
def txt2json():
    dic = {}
    for i in range(1, 1501):
        path = f"../test/{i}/feature.txt"
        ans_list = []
        f = open(path, 'r')
        for line in f:
            ls = (list(map(float, line.split(" "))))
            ls[0] = round(ls[0], 4)
            ls[1] = round(ls[1], 4)
            ls[2] = round(ls[2])
            ans_list.append(ls)
        dic[f"{i}"] = ans_list
    with open("../test/answer.json", 'w') as f:
        output_string = json.dumps(dic)
        f.write(output_string)
#}}}

def feature_engineering():
    path = '/Users/loyolaaa/Downloads/MIR-ST500/'
    for i in range(1, 501):
        f = open(path + f"{i}/{i}_feature.json")
        res = open(f"../train/{i}/feature.txt", 'w')
        fea = json.load(f)
        length = len(fea['time'])
        onset = []
        offset= []
        start = -1
        end = -1
        for j in range(length):
            pitch = fea['vocal_pitch'][j]
            if pitch != 0:
                if start == -1:
                    start = j
            else:
                if start != -1:
                    end = j
                    onset.append(start)
                    offset.append(end)
                    start = -1
                    end = -1
        for j in range(len(onset)):
            prev = offset[j-1] if j else 0
            vol = fea['energy'][onset[j]]
            thresh = 8
            while onset[j] > prev and vol / fea['energy'][onset[j]-1] <= thresh:
                onset[j] -= 1
        for j in range(len(offset)):
            nxt = onset[j+1] if j < len(offset)-1 else 10000
            vol = fea['energy'][offset[j]]
            thresh = 8
            while offset[j] < nxt and vol / fea['energy'][offset[j]-1] <= thresh:
                offset[j] += 1

        new_onset = []
        new_offset =[]
        pitch_list = fea['vocal_pitch']
        vol_list = fea['energy']
        for j in range(len(onset)):
            start = onset[j]
            end = offset[j]
            breakpoint = [start]
            for k in range(start, end):
                if vol_list[k] < 1e-5:
                    breakpoint.append(k)

            breakpoint.append(end)
            for i in range(len(breakpoint)-1):
                new_onset.append(breakpoint[i])
                new_offset.append(breakpoint[i+1])

        for j in range(len(new_onset)):
            res.write(f"{fea['time'][new_onset[j]]} {fea['time'][new_offset[j]]} {0}\n")

if __name__ == '__main__':
    feature_engineering()
    F_score("feature.txt", "feature")




