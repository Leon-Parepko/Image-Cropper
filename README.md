# Image-Cropper

`V 1.7 alpha`

This is a simple program, with graphical interface,
which was constructed to prepare images for printing
in separate paper lists. You could configure slice,
border and color settings to print your pictures in
higher (physical) resolution. The program supports
operating on multiple files (in same directory) at
the same time. Also, you could use console mode to
perform operations faster and with higher performance.

## Start:
* Manual

  Before starting the program, make sure you have preinstalled `python 3.7` and all libraries from `REQUIREMENTS.txt`.
  Then you could start the main application by running `Main.py`.


* Auto

  Using Virtual env. you could simply start it by.....


## Working Modes:
#### GUI:
* In this mode you could use graphical interface to interact with application.  

#### CMD:
* This one is used for automation or in case you do not want to use graph. interface. 


## Example:
Here is a simple example of input command and output result:

    "process --i Image-Cropper\Examples\input --o Image-Cropper\Examples\output --m true --b 15 --s 2 1 --c 139 75 154"


* Input:

![](Examples/input/test_img.jpg)


* Output:

![](Examples/output/test_img_(res_1).jpg) ![](Examples/output/test_img_(res_2).jpg)