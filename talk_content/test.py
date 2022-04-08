# 题目2：给定参数n,从1到n会有n个整数1，2，3，...,n这n个数组共有n!种排列，按照大小顺序升序排列出所有列的情况，并一一标记，给定n和k返回第k个值
# 举例：输入n是3，升序排列就是：
# 123
# 132
# 213
# 231
# 312
# 321
# 输入k是2，最后返回第2个值，输出132

# 思路：本地如果如果使用枚举法，暴力解出全排列结果，时间复杂度和空间复杂度过大，这里先排除暴力解。
n = 9
k = 1250

elem_list = [i for i in range(1, n+1)]
divisor_list = [1]

for i in range(2, n):
    divisor_list.append(divisor_list[-1]*i)
divisor_list.sort(reverse=True)

result_list = []
for i in range(len(divisor_list)):
    tmp = (k-1) // divisor_list[i]
    result_list.append(elem_list[tmp])
    elem_list.pop(tmp)
    k = k % divisor_list[i]
    if k == 1:
        break
    if k == 0:
        elem_list.sort(reverse=True)
        break
result_list.extend(elem_list)
print("".join(list(map(str, result_list))))