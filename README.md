# CMD

NOTE: Tested on Window 8.1 with Python 3.5.2

Before running edit options_dir on the 10th line in the main.py to the directory that you have main.py at. <br>
(Remember to use \\ for single slashed like I did it.)

You can execute the program using 2 ways. The first one is to run it in the directory the file is located. <br>
So if you want to run and use the program from anywhere then you should use method 2:

> 1. Using python to execute only in the main.py directory:<br>
  In the command line run it using:<br>
  python main.py {filename} {new/open} {path doesn't work}

> 2. Execute from anywhere using batch: <br>
  To run it anywhere you will need to make a batch file that links it and passes the args.<br>
  Then you can add the folder with the batch file to environmental variables.<br>
  You can later call the name of the .bat anywhere.<br>
  So if editor.bat links with the main.py then you can call it:<br>
  editor {arg1} {arg2}<br>
  editor {filename} {new/open}


Read about it on https://arturwagnerbusiness.github.io/
