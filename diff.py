src = "../2/2.txt"
dst = "../2/output.txt"

src_list = []
dst_list = []
src = open(src, 'r')
dst = open(dst, 'r')
for line in src:
    src_list.append(list(map(float, line.split(" ")[:3])))
for line in dst:
    dst_list.append(list(map(float, line.split(" ")[:3])))

p_sum = 0
p_tot = 0
n_sum = 0
n_tot = 0
for i in range(len(src_list)):
    for j in range(len(dst_list)):
        if (abs(src_list[i][0] - dst_list[j][0]) <= 0.1):
            print(dst_list[j][0] - src_list[i][0], dst_list[j][1] - src_list[i][1], dst_list[j][2] - src_list[i][2])
            if (dst_list[j][0] > src_list[i][0]):
                p_tot += 1
                p_sum += dst_list[j][0] - src_list[i][0]
            else:
                n_tot += 1
                n_sum += dst_list[j][0] - src_list[i][0]
            break
print(p_sum / p_tot, n_sum / n_tot)
