import codecs
import csv

import numpy as np
import pandas as pd
import xlrd
from numpy.random import choice


class Data():

    def __init__(self):
       pass

    '''数组写入excel表'''

    def excelWriter(A, headers):
        data = pd.DataFrame(columns=headers, data=A)
        writer = pd.ExcelWriter('b.xlsx')  # 写入Excel文件
        data.to_excel(writer, 'page_1', float_format='%.5f', index=True, header=True,
                      )  # ‘page_1’是写入excel的sheet名
        writer.save()
        writer.close()

    def xlsx_to_csv(self):
        workbook = xlrd.open_workbook('b.xlsx')
        table = workbook.sheet_by_index(0)
        with codecs.open('b.csv', 'w', encoding='utf-8') as f:
            write = csv.writer(f)
            for row_num in range(table.nrows):
                row_value = table.row_values(row_num)
                write.writerow(row_value)

    # 订单到达时间
    def data(self, headers):
        time = [1]
        a = 1
        for i in range(0, 149):
            n = choice([0, 1, 2],
                       p=[0.4, 0.3, 0.3])
            a += n
            time.append(a)
        arrive_time = np.array(time)

        customer_level = choice([1, 2, 3], size=150, p=[0.5, 0.3, 0.2])

        delay_time = choice([3, 4, 5, 6],
                            size=150,
                            p=[0.2, 0.3, 0.3, 0.2])

        lead_time_1 = choice([1, 2, 3],
                             size=150,
                             p=[0.5, 0.3, 0.2])

        lead_time_2 = choice([1, 2, 3],
                             size=150,
                             p=[0.5, 0.3, 0.2])

        lead_time_3 = choice([1, 2, 3],
                             size=150,
                             p=[0.5, 0.3, 0.2])

        lead_time_4 = choice([1, 2, 3],
                             size=150,
                             p=[0.5, 0.3, 0.2])

        daily_capacity_1 = choice([1, 2, 3],
                                  size=150,
                                  p=[0, 1, 0])

        daily_capacity_2 = choice([1, 2, 3],
                                  size=150,
                                  p=[0, 1, 0])

        daily_capacity_3 = choice([1, 2, 3],
                                  size=150,
                                  p=[0, 1, 0])

        daily_capacity_4 = choice([1, 2, 3],
                                  size=150,
                                  p=[0, 1, 0])

        revenue = choice([3, 4, 5, 6],
                         size=150,
                         p=[0.2, 0.3, 0.3, 0.2])
        data = np.transpose(np.vstack((arrive_time, customer_level, delay_time, lead_time_1, lead_time_2,
                                             lead_time_3, lead_time_4, daily_capacity_1, daily_capacity_2,
                                             daily_capacity_3, daily_capacity_4, revenue)))
        order_data = pd.DataFrame(columns=headers, data=data)

        return order_data


if __name__ == '__main__':
    headers = ['arrival_time', 'customer_level', 'delay_time', 'lead_time_1', 'lead_time_2',
               'lead_time_3', 'lead_time_4', 'daily_capacity_1', 'daily_capacity_2', 'daily_capacity_3',
               'daily_capacity_4',
               'revenue']
    data = Data()
    order_data = data.data(headers)

