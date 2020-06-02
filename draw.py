import os, json
import numpy as np
import matplotlib.pyplot as plt

def main():
    for i in range(1, 501):
        src = open(f"../train/{i}/{i}.txt", 'r')
        src_list = []
        for line in src:
            src_list.append(list(map(float, line.split(" ")[:3])))
    arr = []
    for x in src_list:
        arr.append(round(100*(x[1]-x[0])))
    plt.hist(arr, bins=50)
    for i in range(1, 501):
        src = open(f"../train/{i}/combine.txt", 'r')
        src_list = []
        for line in src:
            src_list.append(list(map(float, line.split(" ")[:3])))
    arr = []
    for x in src_list:
        arr.append(round(100*(x[1]-x[0])))
    plt.hist(arr, bins=50)
    plt.show()

def check_bias():
    gt_list = []
    for i in range(1, 501):
        gt = open(f"../train/{i}/{i}.txt", 'r')
        for line in gt:
            gt_list.append(list(map(float, line.split(" ")[:3])))
    src_list = []
    for i in range(1, 501):
        src = open(f"../train/{i}/combine.txt_log", 'r')
        for line in src:
            src_list.append(list(map(float, line.split(" ")[:6])))

    arr_true = []
    arr_false = []
    for x in src_list:
        Min = 10000
        ans = -1
        for y in gt_list:
            if abs(x[0] - y[0]) < Min:
                Min = abs(x[0] - y[0])
                ans = x[0]-y[0]
            else:
                break
        if ans > 0:
            arr_true.append(round(100*(ans)))
        else:
            arr_false.append(round(100*(ans)))
    print(np.mean(np.array(arr_true)), len(arr_true))
    print(np.mean(np.array(arr_false)), len(arr_false))
    plt.hist(arr_true, bins=200, color='blue')
    plt.hist(arr_false, bins=200, color='red')
    plt.show()


def check_log():
    for i in range(1, 501):
        src = open(f"../train/{i}/combine.txt_log", 'r')
        src_list = []
        for line in src:
            src_list.append(list(map(float, line.split(" ")[:6])))
    arr_true = []
    arr_false = []
    for x in src_list:
        if x[3]:
            arr_true.append(round(100*(x[1]-x[0])))
        else:
            arr_false.append(round(100*(x[1]-x[0])))
    plt.hist(arr_true, bins=200, color='blue')
    plt.hist(arr_false, bins=200, color='red')
    plt.show()



if __name__ == '__main__':
    #main()
    #check_log()
    check_bias()




