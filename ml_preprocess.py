import json
import numpy as np
    
def preprocess():
    seg_len = 2000 ## 60s
    stride = 200
    step = 0.032
    train_X = []
    train_Y = []
    valid_X = []
    valid_Y = []
    for idx in range(1, 501):
        f1 = open(f"../train/{idx}/{idx}_vocal.json")
        f2 = open(f"../train/{idx}/{idx}.txt")
        src = json.load(f1)
        dst = []
        for line in f2:
            dst.append(list(map(float, line.split(" ")[:3])))
        train = []
        answer= []
        now = 0.016
        dst_now = 0
        for item in src:
            pitch = item[1]
            train.append(pitch)
            while dst_now < len(dst)-1 and now > dst[dst_now][1]:
                dst_now += 1
            if now < dst[dst_now][0]:
                answer.append(0)
            elif now < dst[dst_now][1]:
                answer.append(dst[dst_now][2])
            else:
                answer.append(0)
            now += step
    
        while len(train) % stride != 0 or len(train) < seg_len:
            train.append(0)
            answer.append(0)
        assert len(answer) % stride == 0
        assert len(answer) >= seg_len
        for i in range(seg_len-1, len(train), stride):
            train_slice = train[i-(seg_len-1):i+1]
            ans_slice = answer[i-(seg_len-1):i+1]
            cnt = 0
            for j in train_slice:
                if j == 0:
                    cnt += 1
            if (cnt >= seg_len // 2):
                pass
            else:
                if idx <= 400:
                    train_X.append(train_slice)
                    train_Y.append(ans_slice)
                else:
                    valid_X.append(train_slice)
                    valid_Y.append(ans_slice)
    np.save('train_X', np.array(train_X, dtype=np.float))
    np.save('train_Y', np.array(train_Y, dtype=np.float))
    np.save('valid_X', np.array(valid_X, dtype=np.float))
    np.save('valid_Y', np.array(valid_Y, dtype=np.float))

def array2txt(answer):
    now = 0.016
    k = 0
    start = -1
    end = -1
    pitch = -1
    out = open(f"../train/{idx}/ml.txt", 'w')
    while k < len(answer):
        if answer[k] != 0:
            if start == -1:
                start = now
                pitch = answer[k]
            elif answer[k] != pitch:
                end = now-step
                out.write(f"{start} {end} {pitch}\n") 
                start = now
                end = -1
                pitch = answer[k]
        else:
            if start != -1:
                end = now
                out.write(f"{start} {end} {pitch}\n") 
                end = -1
                start = -1
        k += 1
        now += step

if __name__ == '__main__':
    preprocess()


