# -*- coding: utf-8 -*-
from pybration.Devices.IODevice import IODevice


class DeviceManager(list):
    def __init__(self):
        super(DeviceManager, self).__init__()
        self.current_id = 0

    def append(self, obj: IODevice, id:int=None):
        if id is None:
            obj.info['id'] = self.__issue_id()
            super(DeviceManager, self).append(obj)
            return
        else:
            for i, d in enumerate(self):
                if id == d.info['id']:
                    obj.info['id'] = id
                    self[i] = obj
                    return
            obj.info['id'] = id
            super(DeviceManager, self).append(obj)
            return
        # raise ValueError("please check device id.")

    def delete(self, id:int):
        for idx, d in enumerate(self):
            if d.info['id'] == id:
                self.pop(idx)
                print("%s を削除" % d)

    def __issue_id(self):
        new_id = 0
        for i in self:
            if new_id == i.info['id']:
                new_id += 1
        return new_id

    def extract_device(self,name=None, type=None, id=None)->list:
        device = []
        for i in self:
            if i.info['name'] == name or i.info['type'] == type or i.info['id'] == id:
                device.append(i)
        return device

    def print(self):
        for i in self:
            print(i.info)


class TestDevice(IODevice):
    def __init__(self, c = "None"):
        super(TestDevice, self).__init__()
        self.info['name'] = "TestDevice"
        self.info['type'] = 'TestType'
        self.info['comment'] = c
        # print(self.info)

    def is_open(self):
        return True

    def open_device(self):
        return True

    def close_device(self):
        return True


if __name__ == '__main__':
    test = DeviceManager()
    for i in range(15):
        test.append(TestDevice())

    t_dev = TestDevice()
    test.append(TestDevice("aaaa"), 10)
    test.append(TestDevice())
    test.test()


