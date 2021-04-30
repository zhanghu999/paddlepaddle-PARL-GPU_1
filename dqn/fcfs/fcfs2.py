import numpy as np
import pandas as pd
from data.data_generate_1 import Data


class Fcfs_Order:
    def __init__(self, df):
        CAPACITY_1 = 100  # 工序1产能
        CAPACITY_2 = 100  # 工序2产能
        CAPACITY_3 = 100  # 工序3产能
        CAPACITY_4 = 100  # 工序4产能
        self.df = df  # 数据文件
        self.current_step = 0  # 当前步数
        self.current_capacity_1 = CAPACITY_1  # 每一个阶段有300个产能
        self.current_capacity_2 = CAPACITY_2  # 每一个阶段有300个产能
        self.current_capacity_3 = CAPACITY_3  # 每一个阶段有300个产能
        self.current_capacity_4 = CAPACITY_4  # 每一个阶段有300个产能
        self.need_capacity_1 = 0  # 当前时间下完成所有已接受订单所需要的产能
        self.need_capacity_2 = 0  # 当前时间下完成所有已接受订单所需要的产能
        self.need_capacity_3 = 0  # 当前时间下完成所有已接受订单所需要的产能
        self.need_capacity_4 = 0  # 当前时间下完成所有已接受订单所需要的产能
        self.arrival_time_old = 1  #上一个订单的到达时间，若下一个订单与上一个订单一同达到，则完成当前订单所需要的产能不变


    def accept_order(self):
        arrival_time = self.df.iloc[self.current_step].arrival_time
        lead_time_1 = self.df.iloc[self.current_step].lead_time_1
        lead_time_2 = self.df.iloc[self.current_step].lead_time_2
        lead_time_3 = self.df.iloc[self.current_step].lead_time_3
        lead_time_4 = self.df.iloc[self.current_step].lead_time_4
        delay_time = self.df.iloc[self.current_step].delay_time
        revenue = self.df.iloc[self.current_step].revenue

        # 即使没有订单，产能也会流失
        if self.arrival_time_old != arrival_time:
            self.need_capacity_1 -= (arrival_time - self.arrival_time_old) * 2
            self.need_capacity_2 -= (arrival_time - self.arrival_time_old) * 2
            self.need_capacity_3 -= (arrival_time - self.arrival_time_old) * 2
            self.need_capacity_4 -= (arrival_time - self.arrival_time_old) * 2

            if self.need_capacity_1 < 0:
                self.current_capacity_1 += self.need_capacity_1
                self.need_capacity_1 = 0

            if self.need_capacity_2 < 0:
                self.current_capacity_2 += self.need_capacity_2
                self.need_capacity_2 = 0

            if self.need_capacity_3 < 0:
                self.current_capacity_3 += self.need_capacity_3
                self.need_capacity_3 = 0

            if self.need_capacity_4 < 0:
                self.current_capacity_4 += self.need_capacity_4
                self.need_capacity_4 = 0
        print("工序1剩余产能=%d 完成当前已接受订单需要工序1产能=%d " % (self.current_capacity_1, self.need_capacity_1))
        # print("工序2剩余产能=%d 完成当前已接受订单需要工序2产能=%d " % (self.current_capacity_2, self.need_capacity_2))
        # print("工序3剩余产能=%d 完成当前已接受订单需要工序3产能=%d " % (self.current_capacity_3, self.need_capacity_3))
        # print("工序4剩余产能=%d 完成当前已接受订单需要工序4产能=%d " % (self.current_capacity_4, self.need_capacity_4))
        print("订单属性：到达时间%d 工序1提前期%d 工序2提前期%d 工序3提前期%d 工序4提前期%d 交货期%d 订单收益%d " % (arrival_time, lead_time_1, lead_time_2, lead_time_3, lead_time_4, delay_time, revenue))
        if self.is_able_receive():
            reward = revenue
            self.current_capacity_1 -= lead_time_1  # 工序1当前剩余产能
            self.current_capacity_2 -= lead_time_2  # 工序2当前剩余产能
            self.current_capacity_3 -= lead_time_3  # 工序1当前剩余产能
            self.current_capacity_4 -= lead_time_4  # 工序2当前剩余产能
            self.need_capacity_1 += lead_time_1  # 完成当前订单所需要消耗的产能
            self.need_capacity_2 += lead_time_2  # 完成当前订单所需要消耗的产能
            self.need_capacity_3 += lead_time_3  # 完成当前订单所需要消耗的产能
            self.need_capacity_4 += lead_time_4  # 完成当前订单所需要消耗的产能
            print(" \033[1;35m 接受订单 \033[0m")

        else:
            reward = 0
            print(" \033[1;33m 不满足接受要求的订单 \033[0m")
            print(" \033[1;32m 拒绝订单 \033[0m")

        self.current_step += 1  # 下一订单序列
        self.arrival_time_old = arrival_time

        print("工序1剩余产能=%d 完成当前已接受订单需要产能=%d " % (self.current_capacity_1, self.need_capacity_1))
        # print("工序2剩余产能=%d 完成当前已接受订单需要产能=%d " % (self.current_capacity_2, self.need_capacity_2))
        # print("工序3剩余产能=%d 完成当前已接受订单需要产能=%d " % (self.current_capacity_3, self.need_capacity_3))
        # print("工序4剩余产能=%d 完成当前已接受订单需要产能=%d " % (self.current_capacity_4, self.need_capacity_4))

        return reward

    def is_able_receive(self):
        lead_time_1 = self.df.iloc[self.current_step].lead_time_1  # 工序1提前期
        lead_time_2 = self.df.iloc[self.current_step].lead_time_2  # 工序2提前期
        lead_time_3 = self.df.iloc[self.current_step].lead_time_3  # 工序1提前期
        lead_time_4 = self.df.iloc[self.current_step].lead_time_4  # 工序2提前期
        delay_time = self.df.iloc[self.current_step].delay_time,  # 交货期
        if (lead_time_1 + self.need_capacity_1 - delay_time > 0) or (
                lead_time_2 + self.need_capacity_2 - delay_time > 0) or (
                lead_time_3 + self.need_capacity_3 - delay_time > 0) or (
                lead_time_4 + self.need_capacity_4 - delay_time > 0):  #
            return False  # 拒绝订单
        else:
            return True

    def is_done(self):

        ''' 判断当前是否已经结束 ，当产能使用完后则结束'''
        if self.current_capacity_1 <= 0 or self.current_step > 149 or self.current_capacity_2 <= 0 or self.current_capacity_3 <= 0 or self.current_capacity_4 <= 0:
            done = False
        else:
            done = True
        return done

if __name__ == '__main__':
    headers = ['arrival_time', 'customer_level', 'delay_time', 'lead_time_1', 'lead_time_2',
               'lead_time_3', 'lead_time_4', 'daily_capacity_1', 'daily_capacity_2', 'daily_capacity_3',
               'daily_capacity_4',
               'revenue']
    da = Data()
    df = da.data(headers)
    Fcfs = Fcfs_Order(df)
    total_reward = 0
    while Fcfs.is_done():
        reward =Fcfs.accept_order()
        total_reward += reward
        print("累计收益=%d" %total_reward)
        print("-------------")


