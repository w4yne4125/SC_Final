
def calc(src_path, dst_path):
    src = open(src_path, 'r')
    try:
        dst = open(dst_path, 'r')
    except:
        return
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
    F_COn = [0, 0, 0]
    F_COnP = [0, 0, 0]
    F_COnPOff = [0, 0, 0]
    for i in range(1, 501):
        src_path = f'../{i}/{i}.txt'
        dst_path = f'../{i}/output.txt'
        calc(src_path, dst_path)
    print("---ori---")
    result()
    F_COn = [0, 0, 0]
    F_COnP = [0, 0, 0]
    F_COnPOff = [0, 0, 0]
    for i in range(1, 501):
        src_path = f'../{i}/{i}.txt'
        dst_path = f'../{i}/test.txt'
        calc(src_path, dst_path)
    print("---sam---")
    result()
    F_COn = [0, 0, 0]
    F_COnP = [0, 0, 0]
    F_COnPOff = [0, 0, 0]
    for i in range(1, 501):
        src_path = f'../{i}/{i}.txt'
        dst_path = f'../{i}/combine.txt'
        calc(src_path, dst_path)
    print("---com---")
    result()


