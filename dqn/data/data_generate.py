import codecs
import csv

import numpy as np
import pandas as pd
import xlrd
from numpy.random import choice

headers = ['arrival_time', 'customer_level', 'delay_time', 'lead_time_1', 'lead_time_2',
           'lead_time_3', 'lead_time_4', 'daily_capacity_1', 'daily_capacity_2', 'daily_capacity_3', 'daily_capacity_4',
           'revenue']

'''数组写入excel表'''


def excelWriter(A , headers):
    data = pd.DataFrame(columns=headers, data=A)
    writer = pd.ExcelWriter('b.xlsx')  # 写入Excel文件
    data.to_excel(writer, 'page_1', float_format='%.5f', index=True, header=True,
                  )  # ‘page_1’是写入excel的sheet名
    writer.save()
    writer.close()


def xlsx_to_csv():
    workbook = xlrd.open_workbook('b.xlsx')
    table = workbook.sheet_by_index(0)
    with codecs.open('b.csv', 'w', encoding='utf-8') as f:
        write = csv.writer(f)
        for row_num in range(table.nrows):
            row_value = table.row_values(row_num)
            write.writerow(row_value)


# 订单到达时间
def Arrive_time(num):
    time = [1]
    a = 1
    for i in range(0, num):
        n = choice([0, 1, 2],
                   p=[0.4, 0.3, 0.3])
        a += n
        time.append(a)
    time1 = np.array(time)
    return time1


# 顾客等级
def Customer_level():
    customer_level = choice([1, 2, 3],
                            size=150,
                            p=[0.5, 0.3, 0.2])
    return customer_level


# 订单交货期
def Delay_time():
    delay_time = choice([3, 4, 5, 6],
                        size=150,
                        p=[0.2, 0.3, 0.3, 0.2])
    return delay_time


# 制造单元1提前期
def Lead_time_1():
    lead_time_1 = choice([1, 2, 3],
                         size=150,
                         p=[0.5, 0.3, 0.2])
    return lead_time_1


# 制造单元2提前期
def Lead_time_2():
    lead_time_2 = choice([1, 2, 3],
                         size=150,
                         p=[0.5, 0.3, 0.2])
    return lead_time_2


# 制造单元3提前期
def Lead_time_3():
    lead_time_3 = choice([1, 2, 3],
                         size=150,
                         p=[0.5, 0.3, 0.2])
    return lead_time_3


# 制造单元4提前期
def Lead_time_4():
    lead_time_4 = choice([1, 2, 3],
                         size=150,
                         p=[0.5, 0.3, 0.2])
    return lead_time_4


def Daily_capacity_1():
    daily_capacity_1 = choice([1, 2, 3],
                              size=150,
                              p=[0, 1, 0])
    return daily_capacity_1


def Daily_capacity_2():
    daily_capacity_2 = choice([1, 2, 3],
                              size=150,
                              p=[0, 1, 0])
    return daily_capacity_2


def Daily_capacity_3():
    daily_capacity_3 = choice([1, 2, 3],
                              size=150,
                              p=[0, 1, 0])
    return daily_capacity_3


def Daily_capacity_4():
    daily_capacity_4 = choice([1, 2, 3],
                              size=150,
                              p=[0, 1, 0])
    return daily_capacity_4


# 订单收益
def revenue():
    revenue = choice([3, 4, 5, 6],
                     size=150,
                     p=[0.2, 0.3, 0.3, 0.2])
    return revenue


if __name__ == '__main__':
    arrive_time = Arrive_time(149)
    customer_level = Customer_level()
    delay_time = Delay_time()
    lead_time_1 = Lead_time_1()
    lead_time_2 = Lead_time_2()
    lead_time_3 = Lead_time_3()
    lead_time_4 = Lead_time_4()

    daily_capacity_1 = Daily_capacity_1()
    daily_capacity_2 = Daily_capacity_2()
    daily_capacity_3 = Daily_capacity_3()
    daily_capacity_4 = Daily_capacity_4()
    revenue = revenue()

    order_data = np.transpose(np.vstack((arrive_time, customer_level, delay_time, lead_time_1, lead_time_2,
                                         lead_time_3, lead_time_4, daily_capacity_1, daily_capacity_2,
                                         daily_capacity_3, daily_capacity_4, revenue)))
    excelWriter(order_data,headers)
    xlsx_to_csv()
