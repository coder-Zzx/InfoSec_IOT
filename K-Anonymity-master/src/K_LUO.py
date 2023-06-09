import pandas

cls = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship',
       'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'label']  # 数据属性
QID = ['age', 'workclass', 'education', 'marital-status', 'race', 'sex', 'native-country']

from time import sleep
import math
from model import *
import os
import pandas as pd
import time

data = []
TreeDict = GetTreesDict()
k = 5

## 用于存储最终结果
result = pd.DataFrame(columns=QID)
precision = 0


def Init():
    """
    初始化，生成树,设置阈值，初始化要匿名的属性值
    :return: 所有数据元祖，阈值，所有属性的树
    """

    # 第一步：读取数据，生成元组
    path = os.path.abspath('..')  # 表示当前所处的文件夹上一级文件夹
    data_path = path + '/data/1000.csv'
    # data_path = path + '/data/data_new.txt'

    data_file = open(data_path, 'r')
    lines = data_file.readlines()
    num = 0
    for line in lines:
        i = line[:-1].split(',')
        data.append(i)
        num += 1
        if num > 500:
            break
    return data


if __name__ == '__main__':

    # 【1】初始化数据
    data = Init()
    # 【2】K值要大于等于2
    if k < 2:
        print("参数k不能小于2")
        exit()

    data_len = len(data)

    # 【2】初始数据集如果小于K，则直接退出
    if data_len < k:
        print("数据总量小于匿名数量，无法满足条件")
        exit()

    raw_data = pd.DataFrame(data, columns=QID)
    tmp_data = raw_data.copy()

    print(tmp_data)

    ## 计算程序运行时间
    start = time.time()

    while True:
        #     【1】 对原始数据进行拷贝后，进行K匿名检测
        k_check_res = Test_K_Anonymity(tmp_data, QID, k)
        k_sum = sum(k_check_res)  ## 计算tmp_data 中满足 k 匿名的数据条数
        total_items = tmp_data.shape[0]
        if k_sum == total_items:
            ## 满足K匿名条件, 将数据加入到最终结果集，并停止运行
            print("满足最终K匿名，停止运算")
            result.append(tmp_data)
            break
        elif total_items <= k:  ## 数据总条数是否小于等于 K值，若是则全部泛化为最高层级，并加入最终结果集
            print("数据条数小于K，则进行最高级泛化")
            gen_data = final_generalize(TreeDict, tmp_data.columns, tmp_data)
            tmp_res = result.copy().append(gen_data)  ## 将泛化后的数据，加入到最终结果集，并判断是否满足K匿名
            # tmp_res = result.copy()
            # pandas.concat(tmp_res, gen_data)
            tmp_check_res = Test_K_Anonymity_One_Hot(tmp_res, QID, k)
            # tmp_check_res = Test_K_Anonymity(tmp_res, QID, k)
            tmp_sum = sum(tmp_check_res)
            if tmp_sum == tmp_res.shape[0]:  ## 若满足K匿名条件，则输出最终结果，否则不做任何处理
                result = tmp_res
                print("剩余数据进行最高级泛化后，加入最终结果集，仍然满足K匿名条件，停止运算")
            else:
                print("剩余数据进行最高级泛化后，加入最终结果集,无法满足K匿名条件，停止运算")
            break
        else:  ## 数据条数> K， 则将满足K匿名的数据条目全部抽取到最终结果后，执行第三步
            # print("数据条数 > K， 将数据集中的，满足K匿名的样本，提取到最终结果集中")

            satisfy = tmp_data.loc[k_check_res]
            result = result.append(satisfy)
            # pandas.concat(result, satisfy)

            for tmp_index in range(len(k_check_res)):
                k_check_res[tmp_index] = not k_check_res[tmp_index]

            tmp_data = tmp_data.loc[k_check_res]  ## 提取后，获得提取后的数据

            '''
            第三步，属性集长度为n，选择n-1个属性组成n种集合的元组，统计出各元组中存在的等价类的个数，
            并取等价类数量最大的元组属性的补集进行泛化，所泛化的属性值是元组中等价类对应的数据项中的属性值，
            将泛化后的结果返回到第一步进行K匿名检测
            '''
            equil_num_list = []
            attr_k_check_res_dict = {}
            for i in range(len(QID)):
                tmp_qid = QID.copy()
                tmp_qid.remove(QID[i])
                attr_k_check_res = Test_K_Anonymity(tmp_data, tmp_qid, k)
                equil_num = sum(attr_k_check_res)
                equil_num_list.append(equil_num)
                attr_k_check_res_dict[i] = attr_k_check_res

            '''
            选择待泛化的属性列，规则为：
            存在等价类数据多的列，若等价类数目一样，则选择属性取值多的那一个进行泛化
            '''
            equil_max = max(equil_num_list)
            selected_attr_num = 0
            attr_num = 0
            for i in range(len(equil_num_list)):
                if equil_num_list[i] == equil_max:
                    tmp_attr_num = len(set(tmp_data[QID[i]]))  ## 如果等价类个数满足条件，则计算属性值类型个数
                    if tmp_attr_num > attr_num:
                        attr_num = tmp_attr_num
                        selected_attr_num = i

            ## 对选择的属性列进行泛化，并重新运行整个过程
            # generalize(tree_dict, gen_col, data, index_boolean)
            index_boolean = attr_k_check_res_dict[selected_attr_num]
            ## 异常情况，当所有的数据均没有等价类时，要泛化选中属性的所有样本
            if equil_max == 0:
                for tmp_index in range(len(index_boolean)):
                    index_boolean[tmp_index] = not index_boolean[tmp_index]

            tmp_data = generalize(TreeDict, QID[selected_attr_num], tmp_data, index_boolean)

            # print("泛化属性列为" + QID[selected_attr_num] + ", 泛化后的结果为：")
            # print(tmp_data)

    end = time.time()
    print('\n\n泛化总运行时长为:\n' + str(end - start))
    print('\n\n最终泛化结果如下:\n')
    print(result)
    Save2File(result)

    '''
    计算数据的损失
    '''
    total_loss = 0.0
    total_loss_2 = 0.0
    m, n = result.shape

    # print(tmp_raw_data)

    for j in range(n):
        tree = TreeDict.get(QID[j])
        for i in range(m):
            # print(result.iloc[i][j])
            total_loss += GetLoss(tree, result.iloc[i][j])
            total_loss_2 += GetHeightLoss(tree, result.iloc[i][j])

    print("total_loss=" + str(total_loss))
    print("total_loss_2=" + str(total_loss_2))

    precision_1 = 1.0 - total_loss / (m * n * 1.0)
    precision_2 = 1.0 - total_loss_2 / (m * n * 1.0)

    print("precision_1=" + str(precision_1))
    print("precision_2=" + str(precision_2))
