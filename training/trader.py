import random
class trader:
    '''
    交易员类
    '''
    def __init__(self,gen, no,brain_num, genius,temp, change):
        '''
        创造一个新的交易员
        :param gen:代数
        :param no:编号
        :param brain_num:参数个数
        :param genius:基因库
        :param change:变异率
        '''
        self.gen = gen
        self.result_score = 1
        self.no = no
        self.think = []
        self.cang = 0
        # 选择父母
        father_index = int(random.random()*(len(genius)-1))
        father = genius[father_index]
        mother_index = int(random.random()*(len(genius)-1))
        mother = genius[mother_index]
        # good = temp[father_index]/(temp[father_index]+temp[mother_index])
        good = 0.5
        for i in range(brain_num):
            self.think.append((father[i]*good+mother[i]*(1-good)) + (random.random()*2-1)*change)
        self.signal_list = []
    def trade(self,data,get_result = True):
        '''
        做出交易决定
        :param data: 交易数据
        :param get_result:是否直接获取结果
        '''
        self.think_score = 0
        data = list(data)
        for i in range(len(self.think)):
            while data[i] >1:
                data[i] = data[i]/10
            self.think_score += self.think[i]*data[i]
        average1 = sum(self.think)/len(self.think)
        average2 = sum(data[:-1])/len(data[:-1])
        if self.think_score > average1*average2*10:
            self.signal = 'sell'
        else:
            self.signal = 'buy'
        # print(f'第{self.gen}代第{self.no}号交易员，决策指数为{self.think_score}，信号为{self.signal}',end='')
        if get_result:
            self.get_result(data[-1])
        self.signal_list.append(self.signal)
    def get_result(self,result):
        if self.signal == 'buy':
            if self.cang < 1:
                self.cang += 0.1
            if result == 0 :
                self.result_score -= 10*self.cang
                return 1
            if result < 1:
                self.result_score = self.result_score-1/result*self.cang
            if result > 1:
                self.result_score = self.result_score + result*self.cang
        if self.signal == 'sell':
            if self.cang > -1:
               self.cang -= 0.1
            if result == 0 :
                self.result_score += 10*self.cang
                return 1
            if result < 1:
                self.result_score = self.result_score+1/result*self.cang
            if result > 1:
                self.result_score = self.result_score - result*self.cang
        # print(f'最终得分{self.result_score}')