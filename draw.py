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
    check_log()




