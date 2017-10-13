class Queue:
    value = []

    def __init__(self, size=1, init_val=0):
        self.value = [init_val]*size

    def push(self, val):
        pop_val = self.value[0]
        self.value = [self.value[i+1] for i in range(len(self.value)-1)]
        self.value.append(val)
        return pop_val

    def pop(self):
        pop_val = self.value[0]
        self.value = [self.value[i+1] for i in range(len(self.value)-1)]
        return pop_val
