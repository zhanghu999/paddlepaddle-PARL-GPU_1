import gym
import pandas as pd
from gym import spaces
import numpy as np
from data.data_generate_1 import Data
# 拆分产能，讲产能拆分为两个

class CustomEnv(gym.Env):
    # metadata = {'render.modes' : ['human']}
    def __init__(self, df):
        self.df = df
        self.env = Order(df)
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                            np.array([152, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10 , 10, 10, 10, 10, 10]),
                                            dtype=np.int)

    def reset(self, df):
        del self.env
        self.env = Order(df)
        return self.env.observe()

    def step(self, action):
        return self.env.take_action(action)

    def render(self, mode="human", close=False):
        self.env.view()

class Order:
    def __init__(self, df):
        self.OA = []
        CAPACITY_1 = 100  # 工序1产能
        CAPACITY_2 = 100  # 工序2产能
        CAPACITY_3 = 100  # 工序3产能
        CAPACITY_4 = 100  # 工序4产能
        self.df = df      # 数据文件
        self.current_step = 0  # 当前步数
        self.current_capacity_1 = CAPACITY_1  # 工序1总共有100个产能
        self.current_capacity_2 = CAPACITY_2  # 工序2总共有100个产能
        self.current_capacity_3 = CAPACITY_3  # 工序1总共有100个产能
        self.current_capacity_4 = CAPACITY_4  # 工序2总共有100个产能
        self.need_capacity_1 = 0  # 当前时间下完成所有已接受订单所需要工序1的产能
        self.need_capacity_2 = 0  # 当前时间下完成所有已接受订单所需要工序2的产能
        self.need_capacity_3 = 0  # 当前时间下完成所有已接受订单所需要工序1的产能
        self.need_capacity_4 = 0  # 当前时间下完成所有已接受订单所需要工序2的产能
        self.arrival_time_old = 1  # 上一个订单的到达时间，若下一个订单与上一个订单一同达到，则完成当前订单所需要的产能不变

    def observe(self):
        obs = np.array([
            self.df.iloc[self.current_step].arrival_time,          # 订单到达时间
            self.df.iloc[self.current_step].customer_level,        # 顾客等级
            self.df.iloc[self.current_step].delay_time,            # 交货期
            self.df.iloc[self.current_step].lead_time_1,           # 工序1提前期
            self.df.iloc[self.current_step].lead_time_2,           # 工序2提前期
            self.df.iloc[self.current_step].lead_time_3,           # 工序3提前期
            self.df.iloc[self.current_step].lead_time_4,           # 工序4提前期
            self.df.iloc[self.current_step].daily_capacity_1,      # 工序1每日产能
            self.df.iloc[self.current_step].daily_capacity_2,      # 工序2每日产能
            self.df.iloc[self.current_step].daily_capacity_3,      # 工序3每日产能
            self.df.iloc[self.current_step].daily_capacity_4,      # 工序4每日产能
            self.df.iloc[self.current_step].revenue,               # 订单收益
            self.need_capacity_1,                                  # 完成当前已接受订单所需单元1的产能
            self.need_capacity_2,                                  # 完成当前已接受订单所需单元2的产能
            self.need_capacity_3,                                  # 完成当前已接受订单所需单元3的产能
            self.need_capacity_4,                                  # 完成当前已接受订单所需单元4的产能
        ])
        return obs  # 返回当前订单的状态



    def take_action(self, action):
        arrival_time = self.df.iloc[self.current_step].arrival_time
        customer_level = self.df.iloc[self.current_step].customer_level
        lead_time_1 = self.df.iloc[self.current_step].lead_time_1  # 工序1提前期
        lead_time_2 = self.df.iloc[self.current_step].lead_time_2  # 工序2提前期
        lead_time_3 = self.df.iloc[self.current_step].lead_time_3  # 工序3提前期
        lead_time_4 = self.df.iloc[self.current_step].lead_time_4  # 工序4提前期
        daily_capacity_1 = self.df.iloc[self.current_step].daily_capacity_1  # 工序1每日产能
        daily_capacity_2 = self.df.iloc[self.current_step].daily_capacity_2  # 工序2每日产能
        daily_capacity_3 = self.df.iloc[self.current_step].daily_capacity_3  # 工序3每日产能
        daily_capacity_4 = self.df.iloc[self.current_step].daily_capacity_4  # 工序4每日产能
        delay_time = self.df.iloc[self.current_step].delay_time
        revenue = self.df.iloc[self.current_step].revenue


        # 在一段时间内没有订单，产能流失
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
        print("订单属性：到达时间%d 工序1提前期%d 工序2提前期%d 工序3提前期%d 工序4提前期%d 交货期%d 订单收益%d " % (
        arrival_time, lead_time_1, lead_time_2, lead_time_3, lead_time_4, delay_time, revenue))

        if self.is_able_receive():
            action = 1
            self.OA.append(-1)
            print(" \033[1;33m 不满足接受要求的订单 \033[0m")

        if action == 0:  # 接受订单
            # reward = revenue + customer_level*2
            reward = revenue
            self.current_capacity_1 -= lead_time_1  # 工序1当前剩余产能
            self.current_capacity_2 -= lead_time_2  # 工序2当前剩余产能
            self.current_capacity_3 -= lead_time_3  # 工序1当前剩余产能
            self.current_capacity_4 -= lead_time_4  # 工序2当前剩余产能
            self.need_capacity_1 += lead_time_1     # 完成当前订单所需要消耗的产能
            self.need_capacity_2 += lead_time_2  # 完成当前订单所需要消耗的产能
            self.need_capacity_3 += lead_time_3  # 完成当前订单所需要消耗的产能
            self.need_capacity_4 += lead_time_4  # 完成当前订单所需要消耗的产能

            print(" \033[1;35m 接受订单 \033[0m")
            self.OA.append(1)

        if action == 1:  # 拒绝订单
            reward = 0
            print(" \033[1;32m 拒绝订单 \033[0m")
            self.OA.append(0)

        self.current_step += 1  # 下一订单序列
        self.arrival_time_old = arrival_time
        # print("订单决策后：剩余产能=%d 完成当前已接受订单需要产能=%d " % (self.current_capacity, self.need_capacity))
        done = self.is_done()
        obs = np.array(
            [arrival_time, customer_level, delay_time, lead_time_1, lead_time_2, lead_time_3,lead_time_4,daily_capacity_1, daily_capacity_2, daily_capacity_3,daily_capacity_4, revenue, self.need_capacity_1,self.need_capacity_2,self.need_capacity_3,self.need_capacity_4])
        return obs, reward, done, {}

    def evaluate(self):
        pass

    def is_done(self):
        ''' 判断当前是否已经结束 ，当产能使用完后则结束'''
        if self.current_capacity_1 <= 0 or self.current_step > 149 or self.current_capacity_2 <= 0 or self.current_capacity_3 <= 0 or self.current_capacity_4 <= 0:
            done = True
        else:
            done = False
        return done

    def is_able_receive(self):
        lead_time_1 = self.df.iloc[self.current_step].lead_time_1    # 工序1提前期
        lead_time_2 = self.df.iloc[self.current_step].lead_time_2    # 工序2提前期
        lead_time_3 = self.df.iloc[self.current_step].lead_time_3  # 工序1提前期
        lead_time_4 = self.df.iloc[self.current_step].lead_time_4  # 工序2提前期
        delay_time = self.df.iloc[self.current_step].delay_time,     # 交货期
        if (lead_time_1 + self.need_capacity_1 - delay_time > 0) or (lead_time_2 + self.need_capacity_2 - delay_time > 0) or (lead_time_3 + self.need_capacity_3 - delay_time > 0) or (lead_time_4 + self.need_capacity_4 - delay_time > 0):          #
            return True  # 拒绝订单
        else:
            return False

    def view(self):
        pass

if __name__ == '__main__':
    headers = ['arrival_time', 'customer_level', 'delay_time', 'lead_time_1', 'lead_time_2',
               'lead_time_3', 'lead_time_4', 'daily_capacity_1', 'daily_capacity_2', 'daily_capacity_3',
               'daily_capacity_4',
               'revenue']
    da = Data()
    df = da.data(headers)
    NUM = 1  # 循环次数

    env = CustomEnv(df)
    total_reward = 0
    total_total_reward = 0
    for i in range(NUM):
        env.reset(df)
        for t in range(200):
            action = env.action_space.sample()
            observation, r, done, info = env.step(action)
            total_reward += r

            print("-------------")
            if done:
                print("累计收益=%d" % total_reward)
                print("Episode finished after {} timesteps".format(t + 1))
                print("-------------")
                total_total_reward += total_reward
                total_reward = 0
                break
    average_total_reward = total_total_reward / NUM
    print(average_total_reward)
    print(env.env.OA)
