#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Modified from https://github.com/seungeunrho/minimalRL/blob/master/dqn.py

import random
import collections
import numpy as np


class ReplayMemory(object):

    def __init__(self, max_size):
        # deque 是一个双端队列, 可以从两端append 的数据
        # 队列的长度也就是经验池的容量
        self.buffer = collections.deque(maxlen=max_size)

    def append(self, exp):
        # 往经验池里面添加一条经验
        # 经验以元组的形式进行存储，有状态、动作、奖励、下一个状态以及判断这一条经验是不是这个episode的最后一条经验
        self.buffer.append(exp)

    def sample(self, batch_size):
        # 从经验池当中随机抽取一个batch的数据
        mini_batch = random.sample(self.buffer, batch_size)
        obs_batch, action_batch, reward_batch, next_obs_batch, done_batch = [], [], [], [], []

        for experience in mini_batch:
            s, a, r, s_p, done = experience
            obs_batch.append(s)
            action_batch.append(a)
            reward_batch.append(r)
            next_obs_batch.append(s_p)
            done_batch.append(done)

        return np.array(obs_batch).astype('float32'), \
            np.array(action_batch).astype('float32'), np.array(reward_batch).astype('float32'),\
            np.array(next_obs_batch).astype('float32'), np.array(done_batch).astype('float32')

    def __len__(self):
        return len(self.buffer)
