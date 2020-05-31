import os, json
import numpy as np

def decide_base(seg_list):
    acc = np.zeros(500)
    for x in seg_list:
        acc[len(x)] += 1
    return min(np.argmax(acc), 10) # 有些歌一直連音

def isTail(idx, seg_list):
    # Hard Tail 
    if (idx == len(seg_list) - 1):
        return 1
    if (seg_list[idx+1][0][0] - seg_list[idx][-1][0] >= TailSec):
        return 1
    return 0

def predict_seg(idx, seg_list, base_length, f):
    base_count = max(round(len(seg_list[idx]) / base_length), 1)
    base_len = len(seg_list[idx]) // base_count

    target = seg_list[idx]
    if base_count == 1: # basic situation
        cnt = 0
        acc = 0
        for i in range(len(target) // 2, len(target)):
            cnt += 1
            acc += target[i][1]
        note = round(acc / cnt)
        f.write(f"{target[0][0] - s_bias} {target[-1][0] + e_bias} {note}\n")
        return
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
               note = round(target[i-1][1])
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
                   cnt += 1
                   acc += target[i][1]
               note = round(acc / cnt)
           f.write(f"{target[prev][0] - s_bias} {target[len(target)-1][0] + e_bias} {note}\n")



def F_score(src_file, dst_file):
    global F_COn 
    global F_COnP
    global F_COnPOff
    src = open(src_file, 'r')
    dst = open(dst_file, 'r')
    src_list = []
    dst_list = []
    for line in src:
        src_list.append(list(map(float, line.split(" ")[:3])))
    for line in dst:
        dst_list.append(list(map(float, line.split(" ")[:3])))
    F_COn[0] += len(src_list)
    F_COn[1] += len(dst_list)
    F_COnP[0] += len(src_list)
    F_COnP[1] += len(dst_list)
    F_COnPOff[0] += len(src_list)
    F_COnPOff[1] += len(dst_list)
    for x in dst_list:
        for y in src_list:
            if abs(x[0] - y[0]) <= 0.05:
                F_COn[2] += 1
                break
    for x in dst_list:
        for y in src_list:
            if abs(x[0] - y[0]) <= 0.05 and int(x[2]) == int(y[2]):
                F_COnP[2] += 1
                break
    for x in dst_list:
        for y in src_list:
            if abs(x[0] - y[0]) <= 0.05:
                length = y[1] - y[0]
                offset = max(0.5, 0.2 * length)
                if (int(x[2]) == int(y[2]) and abs(x[1] - y[1]) <= offset):
                    F_COnPOff[2] += 1
                    break


def predict(dir_path, idx):
    json_path = dir_path + "/Vocal.json"
    with open(json_path, 'r') as json_file:
        temp = json.loads(json_file.read())
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
    base_length = decide_base(seg_list)
    file_path = dir_path + "/output.txt"
    ans_path = dir_path + f"/{idx}.txt"
    f = open(file_path, 'w')
    """ --------------------------- """
    
    for i in range(len(seg_list)):
        predict_seg(i, seg_list, base_length, f)

    f.close()
    if not os.path.isfile(dir_path+"/test.txt"):
        return
    F_score(ans_path, dir_path+"/test.txt")

def result():
    global F_COn 
    global F_COnP
    global F_COnPOff
    score1 = 2 * F_COn[2] / (F_COn[0] + F_COn[1])
    score2 = 2 * F_COnP[2] / (F_COnP[0] + F_COnP[1])
    score3 = 2 * F_COnPOff[2] / (F_COnPOff[0] + F_COnPOff[1])
    print(f"F_COn : {F_COn[0]} {F_COn[1]} {F_COn[2]} {score1}\n")
    print(f"F_COnP : {F_COnP[0]} {F_COnP[1]} {F_COnP[2]} {score2}\n")
    print(f"F_COnPOff : {F_COnPOff[0]} {F_COnPOff[1]} {F_COnPOff[2]} {score3}\n")
    print(f"Overall : {0.2 * score1 + 0.6 * score2 + 0.2 * score3}\n")

if __name__ == '__main__':
    """ Configs """
    TailSec = 1
    s_bias = 0.05
    e_bias = 0.01
    F_COn = [0, 0, 0]
    F_COnP = [0, 0, 0]
    F_COnPOff = [0, 0, 0]
    continuous_fac = 0.1
    continuous_part = 4
    """ Configs """
    for i in range(1, 500):
        path = f'../{i}'
        predict(path, i)
    result()



