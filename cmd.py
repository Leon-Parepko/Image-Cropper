import func
from datatypes import CMD_Parametr

def start():
        in_str = input()
        command = in_str.split(" ")

        command = list(filter(None, command))
        if command[0] == "exit":
            return False

        elif command[0] == "help":
            print(" HELP: This command simply shows you this window :) \n\n"
                  " PROCESS: This is the main command to perform any img actions.\n\tThe only important thing is obligatory flags (-i, -o)\n\tCheck the flags to get full description \n\t -i  Input file directory. Format: <C:/folder....>\n\t"
                                                                                                                                                                                         " --o  Output file directory. Format: <C:/folder....>\n\t"
                                                                                                                                                                                         " --m  Multiprocessing on/off. Format: <true / false>\n\t"
                                                                                                                                                                                         " --b  Border. Format: <int(0-100)>\n\t"
                                                                                                                                                                                         " --s  Format: <int(1-10 horiz) int(1-10 vert)>\n\t"
                                                                                                                                                                                         " --c  Format: <int(0-255 red) int(0-255 green) int(0-255 blue)>\n\n"
                  " EXIT: This one simply exits the program.")
            return True

        elif command[0] == "process":

            # Read all the flags
            parametres = []
            for param_str in in_str.split("--")[1:]:
                param_str_splitted = list(filter(None, param_str.split(" ")))
                param = CMD_Parametr(param_str_splitted[0])

                if len(param_str_splitted) == 2:
                    param.add_param(param_str_splitted[1])

                elif len(param_str_splitted) > 2:
                    param.add_params(param_str_splitted[1:])

                else:
                    print(f"No arguments for '{param_str_splitted[0]}' flag!")
                    return True

                parametres.append(param)

            # Configure variables
            cwd = None
            out_wd = None
            border_param = 0
            split_param = [1, 1]
            color_rgb = [0, 0, 0]
            multiproc = False

            out_wd_check = False
            in_wd_check = False
            for elem in parametres:
                if elem.param is None:
                    print("Wrong syntax")
                    return True

                else:
                    # Input dir
                    if elem.flag == "i":
                        in_wd_check = True
                        cwd = elem.get_param()

                    # Output dir
                    elif elem.flag == "o":
                        out_wd_check = True
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
            if out_wd_check and in_wd_check and out_wd != cwd:
                func.process(border_param, split_param, color_rgb, cwd, out_wd, multiproc)
                print('Finished!')
                return True

            else:
                print("Obligatory arguments were not passed!")
                return True

        else:
            print("Wrong syntax")
            return True