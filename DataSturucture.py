#coding:utf-8


class DataContainer:
    def __init__(self):
        self.device = None
        pass

class Plugin:

    def __init__(self):
        self.data = None  #type:DataContainer
        self.parameter = {}
        pass

    def set_parent_data(self, data:DataContainer):
        self.data = data