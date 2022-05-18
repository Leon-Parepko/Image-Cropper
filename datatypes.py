class CMD_Parametr:
    def __init__(self, flag):
        self.flag = flag
        self.param = []


    def add_param(self, data):
        self.param.append(data)


    def add_params(self, data_arr):
        for elem in data_arr:
            self.param.append(elem)


    def get_param(self):
        if len(self.param) == 1:
            return self.param[0]

        elif len(self.param) > 1:
            return self.param