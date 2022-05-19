import os.path


class CMD_Parametr:
    def __init__(self, flag):
        self.flag = flag
        self.param = []


    def add_param(self, data):
        # Input dir
        if self.flag == "i" and os.path.exists(data):
            self.param = data
            return

        # Output dir
        elif self.flag == "o":
            self.param = data
            return


        # Multiprocessing
        elif self.flag == "m" and (data == "true" or data =="false"):
            self.param = data
            return


        # Border
        elif self.flag == "b" and data.isnumeric():
            if 0 <= data <= 100:
                self.param = data
                return

        self.param = None
        return


    def add_params(self, data_arr):
        for elem in data_arr:
            # Split
            if self.flag == "s" and elem.isnumeric():
                if 1 <= elem <= 10 and len(self.param) <= 2:
                    self.param.append(elem)
                else:
                    return

            # Color
            elif self.flag == "c" and elem.isnumeric():
                if 0 <= elem <= 255 and len(self.param) <= 3:
                    self.param.append(elem)
                else:
                    return
                

    def get_param(self):
        if len(self.param) == 1:
            return self.param[0]

        elif len(self.param) > 1:
            return self.param