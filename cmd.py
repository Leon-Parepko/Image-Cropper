import func
from datatypes import CMD_Parametr

def start():
        in_str = input()
        command = in_str.split(" ")

        if command[0] == "exit":
            return False

        elif command[0] == "help":
            print(" HELP: This command simply shows you this window :) \n\n"
                  " PROCESS: This is the main command to perform any img actions.\n\tThe only important thing is obligatory flags (-i, -o)\n\tCheck the flags to get full description \n\t -i  \n\t -o  \n\t -m  \n\t -b \n\t -s  \n\t -c  \n\n"
                  " EXIT: This one simply exits the program.")
            return True

        elif command[0] == "process":

            # Read all the flags
            parametres = []
            for param_str in in_str.split("-")[1:]:
                param_str_splitted = param_str.split(" ")
                param = CMD_Parametr(param_str_splitted[0])
                param.add_params(param_str_splitted[1:])
                parametres.append(param)

            # Configure variables
            cwd = None
            out_wd = None
            border_param = 0
            split_param = [1, 1]
            color_rgb = [0, 0, 0]
            multiproc = False

            for elem in parametres:
                # Input dir
                if elem.flag == "i":
                    cwd = elem.get_param()

                # Output dir
                elif elem.flag == "o":
                    out_wd = elem.get_param()

                # Multiprocessing
                elif elem.flag == "m":
                    multiproc = elem.get_param()

                # Border
                elif elem.flag == "b":
                    border_param = elem.get_param()

                # Split
                elif elem.flag == "s":
                    split_param = elem.get_param()

                # Color
                elif elem.flag == "c":
                    color_rgb = elem.get_param()


            # Perform all operations
            func.process(border_param, split_param, color_rgb, cwd, out_wd, multiproc)







        else:
            print("Wrong syntax")
            return True


