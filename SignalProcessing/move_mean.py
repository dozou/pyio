from Tools.data_structure import *


class MoveMean(Queue):
    def __init__(self, size=1, init_val=0):
        super(MoveMean, self).__init__(size, init_val)

    def push(self, val):
        n = super(MoveMean, self).push(val)
        ans = self.value[0]
        ans = ans-ans
        for i in self.value:
            ans += i
        self.value[len(self.value)-1] = ans/len(self.value)
        return n
