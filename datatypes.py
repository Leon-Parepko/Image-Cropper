import os.path


class CMD_Parametr:
    def __init__(self, flag):
        self.flag = flag
        self.param = None

    def add_param(self, data):
        # Input dir
        if self.flag == "i":
            if data != '' and os.path.exists(data):
                self.param = data
                return

        # Output dir
        elif self.flag == "o" and data != '':
            self.param = data
            return


        # Multiprocessing
        elif self.flag == "m":
            if data.lower() == "true":
                self.param = True
                return

            elif data.lower() == "false":
                self.param = False
                return



        # Border
        elif self.flag == "b" and data.isnumeric():
            data = int(data)
            if 0 <= data <= 100:
                self.param = data
                return

        self.param = None
        return

    def add_params(self, data_arr):

        self.param = []

        for elem in data_arr:
            # Split
            if self.flag == "s" and elem.isnumeric():
                elem = int(elem)
                if 1 <= elem <= 10 and len(self.param) <= 2:
                    self.param.append(elem)
                else:
                    return

            # Color
            elif self.flag == "c" and elem.isnumeric():
                elem = int(elem)
                if 0 <= elem <= 255 and len(self.param) <= 3:
                    self.param.append(elem)
                else:
                    return


    def get_param(self):
        return self.param
